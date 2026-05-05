#!/usr/bin/env python3
"""Generate or verify a strict stage-gate signature for Antseer skill packages.

The signature is not cryptographic identity. It is a deterministic, auditable
review attestation: it records exact file hashes plus strict cross-document
consistency checks. validate_shareable_skill.py refuses Stage 1/2 pass unless
this signature exists, matches current files, and all strict checks pass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

SIGNATURE_FILE = "STAGE-GATE-SIGNATURE.json"
SIGNATURE_VERSION = "1.0"
SIGNABLE_FILES = [
    "SKILL.md",
    "README.md",
    "README.zh.md",
    "skill.meta.json",
    "data-prd.md",
    "skill-prd.md",
    "TECH-INTERFACE-REQUEST.md",
    "TODO-TECH.md",
    "REQUIREMENT-REVIEW.md",
    "review-report.md",
    "mcp-audit.md",
    "data-inventory.md",
    "frontend/index.html",
    "validation.checks.json",
    "stage2-data-sources.example.json",
]
SIGNABLE_DIRS = [
    "layers/L1-data",
    "layers/L2-aggregation",
    "layers/L3-compute",
    "layers/L4-llm",
    "layers/L5-presentation",
    "scripts",
    "agents",
]
IGNORE_NAMES = {SIGNATURE_FILE, ".DS_Store"}
IGNORE_PARTS = {".git", "__pycache__", "node_modules"}
TEXT_EXTS = {".md", ".html", ".json", ".py", ".js", ".ts", ".tsx", ".yaml", ".yml", ".css"}
CODE_TEXT_EXTS = {".py", ".js", ".ts", ".tsx", ".jsx", ".mjs", ".cjs"}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def signable_paths(root: Path) -> list[Path]:
    paths: set[Path] = set()
    for rel in SIGNABLE_FILES:
        p = root / rel
        if rel == "scripts/scaffold_shareable_skill.py":
            continue
        if p.exists() and p.is_file():
            paths.add(p)
    for rel in SIGNABLE_DIRS:
        d = root / rel
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if not p.is_file():
                continue
            r = p.relative_to(root)
            if str(r) == "scripts/scaffold_shareable_skill.py":
                continue
            if p.name in IGNORE_NAMES or any(part in IGNORE_PARTS for part in r.parts):
                continue
            if p.suffix.lower() in TEXT_EXTS:
                paths.add(p)
    return sorted(paths, key=lambda p: str(p.relative_to(root)))


def file_manifest(root: Path) -> dict[str, str]:
    return {str(p.relative_to(root)): sha256_file(p) for p in signable_paths(root)}


def package_digest(manifest: dict[str, str]) -> str:
    blob = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def count_pattern(text: str, pattern: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE | re.MULTILINE))


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(p, text, flags=re.IGNORECASE | re.MULTILINE) for p in patterns)


def load_json(path: Path) -> Any | None:
    try:
        return json.loads(read_text(path))
    except Exception:
        return None


def checks_for_stage(root: Path, stage: str) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, detail: str, severity: str = "critical") -> None:
        checks.append({"id": check_id, "ok": bool(ok), "severity": severity, "detail": detail})

    def contains_heading(text: str, headings: list[str]) -> bool:
        for heading in headings:
            pattern = r"^\s{0,3}#{1,6}\s+" + re.escape(heading) + r"\b"
            if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE):
                return True
        return False

    def unresolved_placeholders(text: str) -> list[str]:
        patterns = [
            r"\{\{[^}]+\}\}",
            r"\bFILL_BEFORE_VALIDATE\b",
            r"\bReplace this\b",
            r"\bYYYY-MM-DD\b",
            r"\{skill-name\}",
            r"\{remote-head-sha\}",
            r"\{synced-at\}",
            r"\{tool-name\}",
            r"\{module-name\}",
        ]
        hits: list[str] = []
        for i, line in enumerate(text.splitlines(), start=1):
            # Literal placeholder examples in documentation or scaffold source
            # code are part of the creator's own validation machinery, not
            # unresolved placeholders in a generated package.
            if any(token in line for token in ["`TODO`", "`Replace this`", "`{{", "`{skill-name}`", "`{remote-head-sha}`", "`{tool-name}`", "`{module-name}`"]):
                continue
            if "FILL_BEFORE_VALIDATE" in line or "YYYY-MM-DD" in line:
                continue
            if "content.replace(" in line and "{{" in line:
                continue
            for pattern in patterns:
                if re.search(pattern, line, flags=re.IGNORECASE):
                    hits.append(f"line {i}: {line.strip()[:120]}")
                    break
        return hits

    def product_plan_exists() -> bool:
        patterns = [
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
            "docs*",
        ]
        for pattern in patterns:
            if list(root.glob(pattern)) or list(root.rglob(pattern)):
                return True
        return False

    def input_schema_valid() -> bool:
        meta_obj = load_json(root / "skill.meta.json")
        if not isinstance(meta_obj, dict):
            return False
        schema = meta_obj.get("input_schema")
        if schema in (None, {}):
            return True
        if not isinstance(schema, dict) or set(schema.keys()) != {"zh", "en"}:
            return False
        zh = schema.get("zh")
        en = schema.get("en")
        if not isinstance(zh, dict) or not isinstance(en, dict) or set(zh.keys()) != set(en.keys()):
            return False
        required = {"type", "label", "default", "options", "description", "required"}
        for key in zh:
            z = zh[key]
            e = en[key]
            if not isinstance(z, dict) or not isinstance(e, dict):
                return False
            if not required.issubset(z.keys()) or not required.issubset(e.keys()):
                return False
            if z["type"] != e["type"] or z["default"] != e["default"] or z["required"] != e["required"]:
                return False
            if not isinstance(z["required"], bool) or not isinstance(e["required"], bool):
                return False
            if not isinstance(z["options"], list) or not isinstance(e["options"], list):
                return False
            if [opt.get("value") for opt in z["options"] if isinstance(opt, dict)] != [opt.get("value") for opt in e["options"] if isinstance(opt, dict)]:
                return False
            if z["type"] == "input" and z["options"] != []:
                return False
            if z["type"] == "select" and z["default"] not in [opt.get("value") for opt in z["options"] if isinstance(opt, dict)]:
                return False
            if z["type"] == "multiple":
                allowed = [opt.get("value") for opt in z["options"] if isinstance(opt, dict)]
                if not isinstance(z["default"], list) or any(item not in allowed for item in z["default"]):
                    return False
        return True

    def has_table(text: str) -> bool:
        return bool(re.search(r"^\|.+\|.+\|.+\|$", text, flags=re.MULTILINE))

    def frontend_files() -> list[Path]:
        candidates: list[Path] = []
        for rel in ["frontend/index.html", "demo-v0.html"]:
            p = root / rel
            if p.exists():
                candidates.append(p)
        return candidates

    def has_frontend_sot_evidence() -> bool:
        evidence = "\n".join(
            read_text(root / rel)
            for rel in [
                "README.md",
                "README.zh.md",
                "review-report.md",
                "TODO-TECH.md",
                "TECH-INTERFACE-REQUEST.md",
                "data-prd.md",
                "skill-prd.md",
                "MCP-COVERAGE.md",
            ]
        )
        return (
            ("antseer-components" in evidence or "Frontend SoT" in evidence or "前端 SoT" in evidence)
            and bool(re.search(r"\b[0-9a-f]{7,40}\b", evidence, flags=re.IGNORECASE))
            and bool(re.search(r"(deviation|gap|blocker|偏差|缺口|整改|Stage 2|阶段 2)", evidence, flags=re.IGNORECASE))
        )

    def s5_present() -> bool:
        return any((root / rel).exists() for rel in ["data-prd.md", "skill-prd.md", "mcp-audit.md", "frontend", "layers"])

    def no_user_path_mocks() -> bool:
        # Use code-shaped patterns rather than broad documentation words.
        # A meta-skill can explain "mock" policy in README/SKILL.md while still
        # having no mock-backed user path.
        mock_patterns = [
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
        ignore_parts = {"tests", "test", "fixtures", "fixture", "evals", "examples", "example", "docs", "references", "assets", "templates", "__pycache__", ".git"}
        scan_paths = []
        for p in root.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in CODE_TEXT_EXTS | {".html"}:
                continue
            rel = p.relative_to(root)
            if any(part in ignore_parts for part in rel.parts):
                continue
            scan_paths.append(p)
        for path in scan_paths:
            if path.name == "SKILL.md":
                continue
            text = read_text(path)
            if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in mock_patterns):
                return False
        return True

    readme = read_text(root / "README.md")
    readme_zh = read_text(root / "README.zh.md")
    tech = read_text(root / "TECH-INTERFACE-REQUEST.md")
    data_prd = read_text(root / "data-prd.md")
    skill_prd = read_text(root / "skill-prd.md")

    add("common.skill-md", (root / "SKILL.md").exists(), "SKILL.md must exist.")
    add("common.readme-en", (root / "README.md").exists(), "README.md must exist.")
    add("common.readme-zh", (root / "README.zh.md").exists(), "README.zh.md must exist.")
    add("common.input-schema", input_schema_valid(), "skill.meta.json input_schema must follow the bilingual standard.")
    add(
        "common.no-unresolved-placeholders",
        not any(unresolved_placeholders(read_text(p)) for p in signable_paths(root) if p.suffix.lower() in TEXT_EXTS),
        "Signable package docs/code must not contain unresolved template placeholders.",
    )

    frontends = frontend_files()
    if frontends:
        add(
            "frontend.inline-json-contract",
            all("id=\"antseer-data\"" in read_text(p) and "id=\"antseer-data-schema\"" in read_text(p) for p in frontends),
            "Frontend templates must expose #antseer-data and #antseer-data-schema.",
        )
        add(
            "frontend.sot-evidence",
            has_frontend_sot_evidence(),
            "Frontend packages must record antseer-components cache commit and Stage 1/2 deviations.",
        )

    if stage == "complete":
        coverage = read_text(root / "MCP-COVERAGE.md")
        add("stage2.version", (root / "VERSION").exists(), "Stage 2 requires VERSION.")
        add("stage2.agent-config", (root / "agents/openai.yaml").exists(), "Stage 2 requires agents/openai.yaml.")
        add("stage2.coverage-file", (root / "MCP-COVERAGE.md").exists(), "Stage 2 requires MCP-COVERAGE.md.")
        add("stage2.readme-data-sources", contains_heading(readme, ["Data Sources"]), "README.md must contain Data Sources for Stage 2.")
        add("stage2.readme-validation", contains_heading(readme, ["Validation Evidence"]), "README.md must contain Validation Evidence for Stage 2.")
        add("stage2.readme-zh-data-sources", contains_heading(readme_zh, ["数据来源"]), "README.zh.md must contain 数据来源 for Stage 2.")
        add("stage2.readme-zh-validation", contains_heading(readme_zh, ["验证证据"]), "README.zh.md must contain 验证证据 for Stage 2.")
        add(
            "stage2.coverage-present",
            bool(coverage) and all(x in coverage.lower() for x in ["verified", "source"]),
            "Stage 2 signature requires MCP-COVERAGE with source and verification evidence.",
        )
        add(
            "stage2.no-user-mock-path",
            no_user_path_mocks(),
            "Stage 2 user path must not depend on mock/stub/fixture/demo/random data.",
        )
    else:
        add("stage1.requirement-review", (root / "REQUIREMENT-REVIEW.md").exists(), "Stage 1 requires REQUIREMENT-REVIEW.md.")
        add("stage1.todo-tech", (root / "TODO-TECH.md").exists(), "Stage 1 requires TODO-TECH.md.")
        add("stage1.tech-interface", (root / "TECH-INTERFACE-REQUEST.md").exists(), "Stage 1 requires TECH-INTERFACE-REQUEST.md.")
        add("stage1.readme-data-reality", contains_heading(readme, ["Data Reality"]), "README.md must contain Data Reality.")
        add("stage1.readme-zh-data-reality", contains_heading(readme_zh, ["数据真实性"]), "README.zh.md must contain 数据真实性.")
        add("stage1.product-plan", product_plan_exists(), "Stage 1 requires a product plan artifact.")
        add("stage1.tech-interface-contracts", bool(tech) and has_table(tech) and any(term in tech.lower() for term in ["mcp", "api", "schema", "接口", "数据"]), "TECH-INTERFACE-REQUEST.md must include concrete MCP/API/data/schema contracts.")
        if s5_present():
            for rel in ["VERSION", "data-prd.md", "skill-prd.md", "review-report.md", "frontend/index.html"]:
                add(f"s5.file.{rel}", (root / rel).exists(), f"S5 semi-finished package requires {rel}.")
            for rel in ["layers/L1-data", "layers/L2-aggregation", "layers/L3-compute", "layers/L4-llm", "layers/L5-presentation"]:
                add(f"s5.dir.{rel}", (root / rel / "README.md").exists(), f"S5 layer requires {rel}/README.md.")
            add("s5.skill-prd-layers", all(token in skill_prd for token in ["L1", "L2", "L3", "L4", "L5", "附录 A"]), "skill-prd.md must explicitly cover L1-L5 and appendix schema.")
            add("s5.data-prd-contract", all(token in data_prd for token in ["P0", "期望接口", "降级", "验收"]), "data-prd.md must include P0, interface expectations, degradation, and acceptance criteria.")

    return checks


def failed_checks(checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [c for c in checks if not c.get("ok") and c.get("severity") == "critical"]


def build_signature(root: Path, stage: str, signer: str, notes: str = "") -> dict[str, Any]:
    manifest = file_manifest(root)
    checks = checks_for_stage(root, stage)
    return {
        "signature_version": SIGNATURE_VERSION,
        "stage": stage,
        "signed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "signer": signer,
        "agent_role": "strict-stage-gate-reviewer",
        "status": "PASS" if not failed_checks(checks) else "FAIL",
        "package_digest": package_digest(manifest),
        "files": manifest,
        "strict_checks": checks,
        "notes": notes,
    }


def verify_signature(root: Path, stage: str) -> tuple[bool, list[str]]:
    path = root / SIGNATURE_FILE
    if not path.exists():
        return False, [f"Missing strict stage-gate signature: {SIGNATURE_FILE}"]
    obj = load_json(path)
    if not isinstance(obj, dict):
        return False, [f"{SIGNATURE_FILE} is not valid JSON object"]
    errors: list[str] = []
    if obj.get("signature_version") != SIGNATURE_VERSION:
        errors.append(f"{SIGNATURE_FILE} signature_version must be {SIGNATURE_VERSION}")
    if obj.get("stage") != stage:
        errors.append(f"{SIGNATURE_FILE} stage mismatch: expected {stage}, got {obj.get('stage')}")
    if obj.get("status") != "PASS":
        errors.append(f"{SIGNATURE_FILE} status must be PASS")
    manifest = file_manifest(root)
    digest = package_digest(manifest)
    if obj.get("package_digest") != digest:
        errors.append(f"{SIGNATURE_FILE} package_digest is stale; rerun strict signing after edits")
    signed_files = obj.get("files")
    if signed_files != manifest:
        errors.append(f"{SIGNATURE_FILE} file manifest is stale or incomplete")
    checks = checks_for_stage(root, stage)
    fails = failed_checks(checks)
    if fails:
        errors.extend(f"Strict signature check failed: {c['id']}: {c['detail']}" for c in fails)
    # Ensure signature recorded the same checks, not a hand-edited PASS.
    recorded = obj.get("strict_checks")
    current_projection = [{"id": c["id"], "ok": c["ok"], "severity": c["severity"], "detail": c["detail"]} for c in checks]
    if recorded != current_projection:
        errors.append(f"{SIGNATURE_FILE} strict_checks are stale; rerun strict signing")
    return not errors, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_path")
    parser.add_argument("--stage", choices=["requirement", "complete"], required=True)
    parser.add_argument("--signer", default="strict-stage-gate-reviewer")
    parser.add_argument("--notes", default="")
    parser.add_argument("--write", action="store_true", help="write STAGE-GATE-SIGNATURE.json if strict checks pass")
    parser.add_argument("--verify", action="store_true", help="verify existing STAGE-GATE-SIGNATURE.json")
    args = parser.parse_args()

    root = Path(args.skill_path).resolve()
    if args.verify:
        ok, errors = verify_signature(root, args.stage)
        if ok:
            print(f"Strict stage-gate signature is valid for stage: {args.stage}")
            return 0
        print(f"Strict stage-gate signature verification failed for stage: {args.stage}\n")
        for e in errors:
            print(f"- {e}")
        return 1

    sig = build_signature(root, args.stage, args.signer, args.notes)
    failures = failed_checks(sig["strict_checks"])
    if failures:
        print(f"Strict stage-gate signing failed for stage: {args.stage}\n")
        for c in failures:
            print(f"- {c['id']}: {c['detail']}")
        return 1

    if args.write:
        (root / SIGNATURE_FILE).write_text(json.dumps(sig, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {SIGNATURE_FILE}")
        print(f"package_digest: {sig['package_digest']}")
    else:
        print(json.dumps(sig, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
