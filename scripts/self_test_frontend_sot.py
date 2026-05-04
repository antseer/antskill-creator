#!/usr/bin/env python3
"""Regression tests for the Antseer frontend Source-of-Truth gate."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from validate_shareable_skill import validate_package  # noqa: E402


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_complete_skill(root: Path) -> None:
    write(
        root / "SKILL.md",
        """---
name: bad-frontend-sot
description: Validate bad frontend SoT gates.
---

# Bad frontend SoT
""",
    )
    write(
        root / "README.md",
        """# Bad frontend SoT

## Data Sources

| Data item | Source | Method | Last verified | Failure handling |
|---|---|---|---|---|
| Price | Verified API | API | 2026-05-04 | Error state |

## Validation Evidence

Verified pass with real API data.
""",
    )
    write(
        root / "README.zh.md",
        """# Bad frontend SoT

## 数据来源

| 数据项 | 来源 | 方法 | 最后验证 | 失败处理 |
|---|---|---|---|---|
| 价格 | 已验证 API | API | 2026-05-04 | 错误态 |

## 验证证据

已通过真实 API 数据验证。
""",
    )
    write(root / "VERSION", "0.0.1\n")
    write(root / "agents" / "openai.yaml", "name: bad-frontend-sot\n")
    write(
        root / "MCP-COVERAGE.md",
        """# MCP Coverage

All data dependencies are verified and covered by API.
""",
    )


def test_bad_stage2_frontend_fails() -> None:
    root = Path(tempfile.mkdtemp(prefix="frontend-sot-bad-"))
    make_complete_skill(root)
    write(
        root / "frontend" / "index.html",
        """<!doctype html>
<html>
<head>
<style>
body, .container { max-width: 960px; margin: 0 auto; padding: 24px; color: #00ffff; }
</style>
</head>
<body>
<main class="container">
  <div id="app">Price</div>
  <script id="antseer-data" type="application/json">{"price":1}</script>
  <script id="antseer-data-schema" type="application/json">{"price":"number"}</script>
  <script src="./app.js"></script>
</main>
</body>
</html>
""",
    )
    write(
        root / "frontend" / "app.js",
        """const fallbackData = {};
function render(rawPayload) {
  return rawPayload.items.map((x) => x.price).reduce((a, b) => a + b, 0);
}
document.body.insertAdjacentHTML('beforeend', 'Powered by Antseer.ai');
""",
    )

    report = validate_package(root, stage="complete", run_checks=False)
    errors = "\n".join(report.errors)
    required_fragments = [
        "package docs must record antseer-components cache commit/evidence",
        "frontend code style missing data adapter layer evidence",
        "frontend design state model must show at least 3 of loading/empty/error/degraded",
        "host-owned outer layout constraint detected",
        "non-canonical hardcoded colors",
        "fabricate fallback/default data",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in errors]
    assert not report.ok, "bad Stage 2 frontend should fail frontend SoT hard gate"
    assert not missing, "missing expected frontend SoT errors: " + ", ".join(missing)


def test_fake_component_commit_fails() -> None:
    root = Path(tempfile.mkdtemp(prefix="frontend-sot-fake-commit-"))
    make_complete_skill(root)
    write(
        root / "README.md",
        """# Bad frontend SoT

antseer-components inspected at commit deadbeef.

## Data Sources

| Data item | Source | Method | Last verified | Failure handling |
|---|---|---|---|---|
| Price | Verified API | API | 2026-05-04 | Error state |

## Validation Evidence

Verified pass with real API data.
""",
    )
    write(
        root / "frontend" / "index.html",
        """<!doctype html>
<html>
<head>
<style>
:root { --antseer-primary: #36DD0C; --antseer-bg: #080807; }
.panel { color: var(--antseer-primary); }
</style>
</head>
<body>
<main class="panel">
  <div id="app">Loading Empty Error Degraded</div>
  <script id="antseer-data" type="application/json">{"price":1}</script>
  <script id="antseer-data-schema" type="application/json">{"price":"number"}</script>
  <script>
    function adaptPayload(payload) { return payload; }
    function calculateSignal(domain) { return domain; }
    function createViewModel(signal) { return { signal }; }
    function render(viewModel) { document.getElementById('app').textContent = JSON.stringify(viewModel); }
    render(createViewModel(calculateSignal(adaptPayload(JSON.parse(document.getElementById('antseer-data').textContent)))));
  </script>
  <footer>Data Source · Powered by Antseer.ai</footer>
</main>
</body>
</html>
""",
    )
    report = validate_package(root, stage="complete", run_checks=False)
    errors = "\n".join(report.errors)
    assert not report.ok, "fake antseer-components commit should not satisfy Stage 2 frontend SoT"
    assert "package docs must record antseer-components cache commit/evidence" in errors


if __name__ == "__main__":
    test_bad_stage2_frontend_fails()
    test_fake_component_commit_fails()
    print("frontend SoT regression tests passed")
