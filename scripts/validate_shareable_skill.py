#!/usr/bin/env python3
"""Validate an AntSkill package against the two-stage lifecycle.

Stage 1 / requirement: complete product plan + mock data clearly declared.
Stage 2 / complete: all user-path mocks replaced by verified real MCP/API/data sources.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from quick_validate import validate_skill

JUNK_PATTERNS = [".DS_Store", "*.pyc"]
JUNK_DIRS = {"__pycache__"}
COMMON_REQUIRED_FILES = ["SKILL.md", "README.md", "README.zh.md"]
REQUIREMENT_REQUIRED_FILES = [
    "REQUIREMENT-REVIEW.md",
    "TODO-TECH.md",
    "TECH-INTERFACE-REQUEST.md",
]
COMPLETE_REQUIRED_FILES = [
    "VERSION",
    "agents/openai.yaml",
    "MCP-COVERAGE.md",
]
REQUIRED_INPUT_SCHEMA_FIELDS = {"type", "label", "default", "options", "description", "required"}
PRODUCT_PLAN_PATTERNS = [
    "*PRD*",
    "*prd*",
    "*spec*",
    "*SPEC*",
    "*prototype*",
    "*Prototype*",
    "*frontend*",
    "*Frontend*",
    "*backend*",
    "*Backend*",
    "design*",
    "docs*",
]
FALSE_DIRECT_USE_CLAIMS = [
    "direct-use ready",
    "ready for" + " production",
    "production" + " ready",
    "直接真实可用",
    "可直接真实可用",
    "可直接用于生产",
]
# Keep these code-shaped to avoid flagging documentation strings that merely
# explain mock/stub concepts. Stage 2 should fail when executable user-path
# logic still defines or calls mock/stub/random demo data.
USER_PATH_MOCK_PATTERNS = [
    r"\bmock_(data|rows|items|response|result|payload|source)\s*=",
    r"\b(stub|fixture)_(data|rows|items|response|result|payload|source)\s*=",
    r"\b(sample|demo|fake|dummy|placeholder)_(data|rows|items|response|result|payload|source)\s*=",
    r"\b(sample|demo|fake|dummy|placeholder)(Data|Rows|Items|Response|Result|Payload|Source)\s*=",
    r"\b(const|let|var)\s+\w*(mock|fake|dummy|placeholder)\w*\s*=",
    r"\bclass\s+(Mock|Fake|Dummy)\w*",
    r"hardcoded[_-]?(data|rows|items|response|result|payload)",
    r"hard-coded[_ -]?(data|rows|items|response|result|payload)",
    r"random\.random\s*\(",
    r"Math\.random\s*\(",
    r"faker\.",
    r"示例数据\s*=",
    r"随机生成\s*\(",
]
CODE_EXTENSIONS = {".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs", ".sql", ".yaml", ".yml", ".json"}
IGNORE_MOCK_SCAN_PARTS = {"tests", "test", "fixtures", "fixture", "evals", "examples", "example", "docs", "references", "assets", "templates"}
PARAM_HINT_PATTERNS = [
    r"\bparameters?\b",
    r"参数",
    r"`--[a-zA-Z0-9-]+`",
    r"\{[a-zA-Z_][a-zA-Z0-9_]*\}",
    r"<[a-zA-Z_][a-zA-Z0-9_-]*>",
]
RUN_CHECKS_FILE = "validation.checks.json"


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    stage: str = "complete"

    @property
    def ok(self) -> bool:
        return not self.errors


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def has_junk(root: Path) -> list[str]:
    found: list[str] = []
    for p in root.rglob("*"):
        rel = p.relative_to(root)
        if any(part in JUNK_DIRS for part in rel.parts):
            found.append(str(rel))
            continue
        if any(fnmatch.fnmatch(p.name, pat) for pat in JUNK_PATTERNS):
            found.append(str(rel))
    return found


def contains_heading(text: str, headings: list[str]) -> bool:
    lowered = text.lower()
    for h in headings:
        if re.search(rf"^#+\s+.*{re.escape(h.lower())}", lowered, re.MULTILINE):
            return True
        if h.lower() in lowered:
            return True
    return False


def detect_stage(root: Path) -> str:
    """Best-effort auto detection. Explicit --stage is preferred.

    README stage markers win over instructional examples inside SKILL.md.
    This keeps meta-skills that document both stages from being misclassified.
    """
    readme = read_text(root / "README.md")
    readme_zh = read_text(root / "README.zh.md")
    readme_blob = f"{readme}\n{readme_zh}"
    readme_lower = readme_blob.lower()

    has_complete_marker = (
        "stage: complete" in readme_lower
        or "stage 2" in readme_lower and "complete" in readme_lower
        or "data sources" in readme_lower
        or "数据来源" in readme_blob
        or (root / "MCP-COVERAGE.md").exists()
    )
    has_requirement_marker = (
        "stage: requirement" in readme_lower
        or "stage 1" in readme_lower and "requirement" in readme_lower
        or "data reality" in readme_lower
        or "数据真实性" in readme_blob
        or (root / "TECH-INTERFACE-REQUEST.md").exists()
    )

    if has_complete_marker and not has_requirement_marker:
        return "complete"
    if has_requirement_marker and not has_complete_marker:
        return "requirement"
    if has_complete_marker and "validation evidence" in readme_lower:
        return "complete"
    if has_requirement_marker:
        return "requirement"

    skill_blob = read_text(root / "SKILL.md")
    skill_lower = skill_blob.lower()
    if "stage 2" in skill_lower and "complete" in skill_lower:
        return "complete"
    if "stage 1" in skill_lower and "requirement" in skill_lower:
        return "requirement"
    return "complete"


def find_product_plan_artifacts(root: Path) -> list[str]:
    found: list[str] = []
    for p in root.rglob("*"):
        if any(part in JUNK_DIRS for part in p.relative_to(root).parts):
            continue
        rel = str(p.relative_to(root))
        if rel in COMMON_REQUIRED_FILES or rel in REQUIREMENT_REQUIRED_FILES or rel in COMPLETE_REQUIRED_FILES:
            continue
        if any(fnmatch.fnmatch(p.name, pat) or fnmatch.fnmatch(rel, pat) for pat in PRODUCT_PLAN_PATTERNS):
            found.append(rel)
    return sorted(set(found))


def scan_user_path_mocks(root: Path) -> list[str]:
    hits: list[str] = []
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix not in CODE_EXTENSIONS:
            continue
        rel = p.relative_to(root)
        if any(part in IGNORE_MOCK_SCAN_PARTS for part in rel.parts):
            continue
        if any(part in JUNK_DIRS for part in rel.parts):
            continue
        text = read_text(p)
        for pattern in USER_PATH_MOCK_PATTERNS:
            if re.search(pattern, text, flags=re.IGNORECASE):
                hits.append(str(rel))
                break
    return sorted(set(hits))


def option_values(options: object) -> list[object]:
    if not isinstance(options, list):
        return []
    values = []
    for opt in options:
        if isinstance(opt, dict) and "value" in opt:
            values.append(opt["value"])
    return values


def validate_input_schema(root: Path) -> list[str]:
    path = root / "skill.meta.json"
    if not path.exists():
        return []

    try:
        obj = json.loads(read_text(path))
    except Exception as e:
        return [f"skill.meta.json is not valid JSON: {e}"]

    if "input_schema" not in obj:
        return []

    schema = obj["input_schema"]
    errors: list[str] = []
    if not isinstance(schema, dict):
        return ["input_schema must be an object"]

    zh = schema.get("zh")
    en = schema.get("en")
    if not isinstance(zh, dict) or not isinstance(en, dict):
        return ["input_schema must contain both zh and en objects"]

    if set(zh.keys()) != set(en.keys()):
        errors.append("input_schema zh/en parameter keys must match exactly")

    for lang, block in [("zh", zh), ("en", en)]:
        for key, cfg in block.items():
            if not isinstance(cfg, dict):
                errors.append(f"input_schema.{lang}.{key} must be an object")
                continue
            missing = REQUIRED_INPUT_SCHEMA_FIELDS - set(cfg.keys())
            if missing:
                errors.append(f"input_schema.{lang}.{key} missing fields: {', '.join(sorted(missing))}")
                continue
            if cfg.get("type") not in {"input", "select", "multiple"}:
                errors.append(f"input_schema.{lang}.{key}.type must be input/select/multiple")
            if not isinstance(cfg.get("options"), list):
                errors.append(f"input_schema.{lang}.{key}.options must be an array")
            else:
                for i, opt in enumerate(cfg["options"]):
                    if not isinstance(opt, dict) or "label" not in opt or "value" not in opt:
                        errors.append(f"input_schema.{lang}.{key}.options[{i}] must contain label and value")
            if not isinstance(cfg.get("required"), bool):
                errors.append(f"input_schema.{lang}.{key}.required must be boolean")
            if cfg.get("type") == "input" and cfg.get("options") != []:
                errors.append(f"input_schema.{lang}.{key}.options must be [] for input type")
            if cfg.get("type") == "select":
                values = option_values(cfg.get("options"))
                if values and cfg.get("default") not in values:
                    errors.append(f"input_schema.{lang}.{key}.default must exist in options[].value for select type")
            if cfg.get("type") == "multiple":
                default = cfg.get("default")
                if not isinstance(default, list):
                    errors.append(f"input_schema.{lang}.{key}.default must be an array for multiple type")
                else:
                    values = option_values(cfg.get("options"))
                    missing_defaults = [v for v in default if v not in values]
                    if values and missing_defaults:
                        errors.append(f"input_schema.{lang}.{key}.default values not found in options[].value: {missing_defaults}")

    for key in set(zh.keys()) & set(en.keys()):
        z = zh.get(key, {})
        e = en.get(key, {})
        if not isinstance(z, dict) or not isinstance(e, dict):
            continue
        for field in ["type", "default", "required"]:
            if z.get(field) != e.get(field):
                errors.append(f"input_schema.{key}.{field} must match between zh and en")
        if option_values(z.get("options")) != option_values(e.get("options")):
            errors.append(f"input_schema.{key}.options[].value must match between zh and en")

    return errors


def maybe_warn_missing_input_schema(root: Path) -> list[str]:
    meta_path = root / "skill.meta.json"
    has_schema = False
    if meta_path.exists():
        try:
            meta = json.loads(read_text(meta_path))
            schema = meta.get("input_schema")
            has_schema = isinstance(schema, dict) and bool(schema.get("zh") or schema.get("en"))
        except Exception:
            has_schema = False
    if has_schema:
        return []

    blob = "\n".join(read_text(root / name) for name in ["SKILL.md", "README.md", "README.zh.md"])
    if any(re.search(pattern, blob, flags=re.IGNORECASE) for pattern in PARAM_HINT_PATTERNS):
        return ["Possible user parameters detected, but skill.meta.json > input_schema is empty or missing"]
    return []


def load_run_checks(root: Path) -> tuple[list[dict], list[str]]:
    path = root / RUN_CHECKS_FILE
    if not path.exists():
        return [], [f"--run-checks requested but {RUN_CHECKS_FILE} is missing"]
    try:
        obj = json.loads(read_text(path))
    except Exception as e:
        return [], [f"{RUN_CHECKS_FILE} is not valid JSON: {e}"]
    checks = obj.get("checks") if isinstance(obj, dict) else None
    if not isinstance(checks, list) or not checks:
        return [], [f"{RUN_CHECKS_FILE} must contain a non-empty checks array"]
    errors = []
    normalized = []
    for i, check in enumerate(checks):
        if not isinstance(check, dict):
            errors.append(f"{RUN_CHECKS_FILE}.checks[{i}] must be an object")
            continue
        name = check.get("name", f"check-{i + 1}")
        command = check.get("command")
        if not isinstance(command, list) or not command or not all(isinstance(x, str) for x in command):
            errors.append(f"{RUN_CHECKS_FILE}.checks[{i}].command must be a non-empty string array")
            continue
        normalized.append({
            "name": str(name),
            "command": command,
            "timeout_seconds": int(check.get("timeout_seconds", 60)),
        })
    return normalized, errors


def run_executable_checks(root: Path) -> list[str]:
    checks, errors = load_run_checks(root)
    if errors:
        return errors
    run_errors = []
    for check in checks:
        try:
            result = subprocess.run(
                check["command"],
                cwd=root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=check["timeout_seconds"],
                check=False,
            )
        except subprocess.TimeoutExpired:
            run_errors.append(f"Run check timed out: {check['name']}")
            continue
        except Exception as e:
            run_errors.append(f"Run check failed to start: {check['name']}: {e}")
            continue
        if result.returncode != 0:
            details = (result.stderr or result.stdout).strip().splitlines()
            snippet = details[-1] if details else "no output"
            run_errors.append(f"Run check failed: {check['name']} exited {result.returncode}: {snippet}")
    return run_errors


def validate_requirement(root: Path) -> list[str]:
    errors: list[str] = []
    readme = read_text(root / "README.md")
    readme_zh = read_text(root / "README.zh.md")
    blob = "\n".join([readme, readme_zh, read_text(root / "SKILL.md")])

    for rel in REQUIREMENT_REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"Stage 1 requirement package missing: {rel}")

    if not contains_heading(readme, ["Data Reality"]):
        errors.append("README.md must contain a Data Reality section for Stage 1")
    if not contains_heading(readme_zh, ["数据真实性"]):
        errors.append("README.zh.md must contain a 数据真实性 section for Stage 1")

    if not find_product_plan_artifacts(root):
        errors.append("Stage 1 requires at least one product plan artifact (PRD/spec/prototype/frontend/backend/docs)")

    lower = blob.lower()
    for claim in FALSE_DIRECT_USE_CLAIMS:
        if claim in lower or claim in blob:
            errors.append(f"Stage 1 must not claim direct-use readiness: found '{claim}'")

    tech_request = read_text(root / "TECH-INTERFACE-REQUEST.md")
    if (root / "TECH-INTERFACE-REQUEST.md").exists():
        needed_terms = ["mcp", "api", "接口", "数据", "schema"]
        if not any(term in tech_request.lower() for term in needed_terms):
            errors.append("TECH-INTERFACE-REQUEST.md should list MCP/API/data/schema requirements")

    return errors


def validate_complete(root: Path, run_checks: bool = False) -> list[str]:
    errors: list[str] = []
    readme = read_text(root / "README.md")
    readme_zh = read_text(root / "README.zh.md")

    for rel in COMPLETE_REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"Stage 2 complete package missing: {rel}")

    if not contains_heading(readme, ["Data Sources"]):
        errors.append("README.md must contain a Data Sources section for Stage 2")
    if not contains_heading(readme, ["Validation Evidence"]):
        errors.append("README.md must contain a Validation Evidence section for Stage 2")
    if not contains_heading(readme_zh, ["数据来源"]):
        errors.append("README.zh.md must contain a 数据来源 section for Stage 2")
    if not contains_heading(readme_zh, ["验证证据"]):
        errors.append("README.zh.md must contain a 验证证据 section for Stage 2")

    coverage = read_text(root / "MCP-COVERAGE.md")
    if (root / "MCP-COVERAGE.md").exists():
        lower = coverage.lower()
        if "mcp" not in lower and "api" not in lower and "数据源" not in coverage:
            errors.append("MCP-COVERAGE.md must describe MCP/API/data-source coverage")
        if not any(term in lower for term in ["verified", "pass", "covered", "验证", "已覆盖", "通过"]):
            errors.append("MCP-COVERAGE.md must include verification status/evidence")

    mock_hits = scan_user_path_mocks(root)
    if mock_hits:
        errors.append("Stage 2 user-path code appears to still contain mock/stub/random data: " + ", ".join(mock_hits))

    validation_blob = readme + "\n" + readme_zh + "\n" + coverage
    if "TODO" in validation_blob or "待补" in validation_blob:
        errors.append("Stage 2 docs must not contain unresolved TODO/待补 placeholders in README or MCP-COVERAGE.md")

    if run_checks:
        errors.extend(run_executable_checks(root))

    return errors


def validate_package(root: Path, stage: str = "auto", run_checks: bool = False) -> ValidationReport:
    actual_stage = detect_stage(root) if stage == "auto" else stage
    report = ValidationReport(stage=actual_stage)

    valid, message = validate_skill(root)
    if not valid:
        report.errors.append(message)

    for rel in COMMON_REQUIRED_FILES:
        if not (root / rel).exists():
            report.errors.append(f"Missing required file: {rel}")

    junk = has_junk(root)
    if junk:
        report.errors.append("Junk files present: " + ", ".join(sorted(junk)))

    report.errors.extend(validate_input_schema(root))
    report.warnings.extend(maybe_warn_missing_input_schema(root))

    if actual_stage == "requirement":
        report.errors.extend(validate_requirement(root))
    elif actual_stage == "complete":
        report.errors.extend(validate_complete(root, run_checks=run_checks))

    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_path")
    parser.add_argument("--stage", choices=["auto", "requirement", "complete"], default="auto")
    parser.add_argument("--run-checks", action="store_true", help=f"For Stage 2, execute commands from {RUN_CHECKS_FILE}")
    args = parser.parse_args()

    root = Path(args.skill_path).resolve()
    report = validate_package(root, stage=args.stage, run_checks=args.run_checks)

    if report.errors:
        print(f"AntSkill package validation failed for stage: {report.stage}\n")
        for e in report.errors:
            print(f"- {e}")
        if report.warnings:
            print("\nWarnings:\n")
            for w in report.warnings:
                print(f"- {w}")
        return 1

    print(f"AntSkill package is valid for stage: {report.stage}")
    if report.warnings:
        print("\nWarnings:\n")
        for w in report.warnings:
            print(f"- {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
