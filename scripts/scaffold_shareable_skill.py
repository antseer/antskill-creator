#!/usr/bin/env python3
"""Scaffold an Skill package using the two-stage lifecycle."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_ROOT / "templates"


def slugify(text: str) -> str:
    text = text.strip().lower().replace("_", "-")
    text = re.sub(r"[^a-z0-9-]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "new-skill"


def render_template(rel_path: str, values: dict[str, str]) -> str:
    path = TEMPLATE_ROOT / rel_path
    content = path.read_text(encoding="utf-8")
    for key, value in values.items():
        content = content.replace("{{" + key + "}}", value)
        content = content.replace("{{ " + key + " }}", value)
        content = content.replace("{" + key.lower().replace("_", "-") + "}", value)
    return content


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def make_skill_meta(skill_name: str, display_name: str, description: str) -> str:
    obj = {
        "id": skill_name,
        "name": display_name,
        "description": description,
        "input_schema": {"zh": {}, "en": {}},
    }
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


def make_requirement_canvas(display_name: str, skill_name: str) -> str:
    return f"""# Requirement Canvas · {display_name}

> Fill every field before entering S1. This scaffold intentionally contains placeholders and must not pass Stage 1 validation until completed.

## Q1 WHO — User

{{{{FILL_BEFORE_VALIDATE}}}}

## Q2 WHAT — Core function / input / output

{{{{FILL_BEFORE_VALIDATE}}}}

## Q3 WHY — Why this skill should exist

{{{{FILL_BEFORE_VALIDATE}}}}

## Q4 WHERE — Data sources

{{{{FILL_BEFORE_VALIDATE}}}}

## Q5 WHEN — Freshness / latency

{{{{FILL_BEFORE_VALIDATE}}}}

## Q6 HOW — Interaction model

{{{{FILL_BEFORE_VALIDATE}}}}

## Q7 PARADIGM — A / B / C

Default: B · specification / semi-finished handoff.

## Boundary confirmation

- [ ] User understands this is a layered semi-finished Antseer skill unless Stage 2 is explicitly validated.
- [ ] L1-B / L2 gaps will be handed to backend through `data-prd.md`.
"""


def make_layer_readme(layer: str) -> str:
    titles = {
        "L1-data": "L1 · 数据接入层",
        "L2-aggregation": "L2 · MCP 聚合接口层",
        "L3-compute": "L3 · Skill 脚本计算层",
        "L4-llm": "L4 · LLM 结构化层",
        "L5-presentation": "L5 · 前端展示层",
    }
    return f"""# {titles.get(layer, layer)}

## 本层职责

{{{{FILL_BEFORE_VALIDATE}}}}

## 责任边界

{{{{FILL_BEFORE_VALIDATE}}}}

## 本 Skill 涉及的 Dxx / 模块

{{{{FILL_BEFORE_VALIDATE}}}}
"""


def make_small_svg(title: str, color: str) -> str:
    short = (title[:2].upper() if title else "SK")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128" fill="none">
  <rect width="128" height="128" rx="28" fill="{color}"/>
  <text x="64" y="74" text-anchor="middle" font-family="Arial, sans-serif" font-size="42" font-weight="700" fill="white">{short}</text>
</svg>
'''


def make_card_svg(title: str, color: str) -> str:
    safe = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630" fill="none">
  <rect width="1200" height="630" rx="40" fill="#0B1020"/>
  <rect x="48" y="48" width="1104" height="534" rx="32" fill="{color}" fill-opacity="0.18" stroke="{color}" stroke-opacity="0.45"/>
  <text x="96" y="250" font-family="Arial, sans-serif" font-size="72" font-weight="700" fill="white">{safe}</text>
  <text x="96" y="330" font-family="Arial, sans-serif" font-size="30" fill="#D1D5DB">Skill Creator Rick two-stage package</text>
</svg>
'''


def build_values(args: argparse.Namespace, skill_name: str, stage: str) -> dict[str, str]:
    stage_line = (
        "Stage 1 Semi-finished Skill：产品方案完整，当前使用 mock 数据展示效果，等待研发接入真实 MCP / API / 数据源。"
        if stage == "requirement"
        else "Stage 2 Finished Skill：用户主路径不再依赖 mock 数据，真实 MCP / API / 数据源已验证可用。"
    )
    return {
        "SKILL_NAME": skill_name,
        "DISPLAY_NAME": args.display_name,
        "SKILL_DISPLAY_NAME": args.display_name,
        "DESCRIPTION": args.description,
        "ONE_LINE_EN": args.one_line_en,
        "ONE_LINE_ZH": args.one_line_zh,
        "BRAND_COLOR": args.brand_color,
        "STAGE_LINE": stage_line,
        "REMOTE_HEAD_SHA": "{{FILL_BEFORE_VALIDATE}}",
        "SYNCED_AT": "{{FILL_BEFORE_VALIDATE}}",
        "TOOL_NAME": "{{FILL_BEFORE_VALIDATE}}",
        "MODULE_NAME": "{{FILL_BEFORE_VALIDATE}}",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("target_dir")
    parser.add_argument("--skill-name", required=True)
    parser.add_argument("--display-name", required=True)
    parser.add_argument("--description", default="Describe what the skill does and when to use it.")
    parser.add_argument("--one-line-en", default="One-line English description.")
    parser.add_argument("--one-line-zh", default="一句话中文说明。")
    parser.add_argument("--stage", choices=["requirement", "complete"], default="requirement")
    parser.add_argument("--brand-color", default="#12C48B")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    stage = args.stage
    skill_name = slugify(args.skill_name)
    values = build_values(args, skill_name, stage)
    target = Path(args.target_dir).resolve()
    if target.exists() and any(target.iterdir()) and not args.force:
        raise SystemExit(f"Target is not empty: {target}. Use --force to overwrite into a non-empty folder.")

    write(target / "SKILL.md", render_template("common/SKILL.md.tmpl", values))
    write(target / "skill.meta.json", make_skill_meta(skill_name, args.display_name, args.description))
    write(target / ".gitignore", ".DS_Store\n__pycache__/\n*.pyc\n.venv/\n")
    write(target / f"assets/{skill_name}-small.svg", make_small_svg(args.display_name, args.brand_color))
    write(target / f"assets/{skill_name}-card.svg", make_card_svg(args.display_name, args.brand_color))

    if stage == "requirement":
        write(target / "README.md", render_template("requirement/README.md.tmpl", values))
        write(target / "README.zh.md", render_template("requirement/README.zh.md.tmpl", values))
        write(target / "REQUIREMENT-REVIEW.md", render_template("requirement/REQUIREMENT-REVIEW.md.tmpl", values))
        write(target / "TODO-TECH.md", render_template("requirement/TODO-TECH.md.tmpl", values))
        write(target / "TECH-INTERFACE-REQUEST.md", render_template("requirement/TECH-INTERFACE-REQUEST.md.tmpl", values))
        write(target / "docs/PRODUCT-SPEC.md", render_template("requirement/PRODUCT-SPEC.md.tmpl", values))
        write(target / "VERSION", "0.1.0\n")
        write(target / "requirement-canvas.md", make_requirement_canvas(args.display_name, skill_name))
        write(target / "demo-v0.html", render_template("s5/skeleton.html", values))
        write(target / "data-inventory.md", render_template("s5/data-inventory-template.md", values))
        write(target / "mcp-audit.md", render_template("s5/mcp-audit-template.md", values))
        write(target / "data-prd.md", render_template("s5/data-prd-template.md", values))
        write(target / "skill-prd.md", render_template("s5/skill-prd-template.md", values))
        write(target / "review-report.md", render_template("s5/review-report-template.md", values))
        write(target / "frontend/index.html", render_template("s5/skeleton.html", values))
        for layer in ["L1-data", "L2-aggregation", "L3-compute", "L4-llm", "L5-presentation"]:
            write(target / "layers" / layer / "README.md", make_layer_readme(layer))
        write(target / "layers/L5-presentation/component-map.md", "# Component Map\n\n{{FILL_BEFORE_VALIDATE}}\n")
    else:
        write(target / "README.md", render_template("complete/README.md.tmpl", values))
        write(target / "README.zh.md", render_template("complete/README.zh.md.tmpl", values))
        write(target / "VERSION", "0.1.0\n")
        write(target / "agents/openai.yaml", render_template("complete/openai.yaml.tmpl", values))
        write(target / ".env.example", render_template("complete/.env.example.tmpl", values))
        write(target / "MCP-COVERAGE.md", render_template("complete/MCP-COVERAGE.md.tmpl", values))

    print(f"Scaffolded Stage {'1 Semi-finished' if stage == 'requirement' else '2 Finished'} package at: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
