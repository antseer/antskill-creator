#!/usr/bin/env python3
"""Sync MCP truth-source docs into local cache, with verified-cache fallback.

Primary path: clone/fetch antseer/third-mcp-server and copy docs/*.md.
Fallback path: if remote access is unavailable but cache/manifest.json and all
cached docs exist, keep the existing cache and exit 0 with an explicit warning.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = "https://github.com/antseer/third-mcp-server.git"
DOCS = [
    "MCP-Data-Capabilities.md",
    "MCP-Tools-Reference.md",
    "MCP-Tools-Query-Type-Mapping.md",
]
TIMEOUT_SECONDS = int(os.environ.get("MCP_SYNC_TIMEOUT", "25"))


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run(cmd: list[str], cwd: Path | None = None) -> str:
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=TIMEOUT_SECONDS,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip().splitlines()
        raise RuntimeError(detail[-1] if detail else f"command failed: {' '.join(cmd)}")
    return result.stdout.strip()


def cache_is_usable(cache_dir: Path) -> bool:
    manifest = cache_dir / "manifest.json"
    if not manifest.exists():
        return False
    try:
        json.loads(manifest.read_text(encoding="utf-8"))
    except Exception:
        return False
    return all((cache_dir / name).exists() and (cache_dir / name).stat().st_size > 0 for name in DOCS)


def resolve_source_repo(repo_dir: Path) -> Path:
    shared_repo = Path("/tmp/antseer-repos/third-mcp-server")
    if shared_repo.exists():
        return shared_repo
    if not repo_dir.exists():
        run(["git", "clone", "--depth", "1", REPO, str(repo_dir)])
        return repo_dir
    run(["git", "fetch", "--depth", "1", "origin"], cwd=repo_dir)
    run(["git", "checkout", "FETCH_HEAD"], cwd=repo_dir)
    return repo_dir


def write_manifest(cache_dir: Path, sha: str, fallback: bool = False) -> None:
    manifest = {
        "repo": "antseer/third-mcp-server",
        "source": REPO,
        "head_sha": sha,
        "fetched_at": now_utc(),
        "fallback_cache": fallback,
        "docs": {name: f"cache/{name}" for name in DOCS},
    }
    (cache_dir / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    cache_dir = root / "mcp-capability-map" / "cache"
    source_repo = cache_dir / "_truth_repo"
    cache_dir.mkdir(parents=True, exist_ok=True)

    try:
        actual_repo = resolve_source_repo(source_repo)
        sha = run(["git", "rev-parse", "HEAD"], cwd=actual_repo)
        for name in DOCS:
            src = actual_repo / "docs" / name
            if not src.exists():
                raise FileNotFoundError(f"Missing docs file in truth repo: {src}")
            shutil.copyfile(src, cache_dir / name)
        write_manifest(cache_dir, sha, fallback=False)
        print(f"Synced MCP truth source to {sha}")
        return 0
    except Exception as exc:
        if cache_is_usable(cache_dir):
            current = json.loads((cache_dir / "manifest.json").read_text(encoding="utf-8"))
            sha = current.get("head_sha", "unknown")
            print(f"WARNING: remote MCP sync failed ({exc}); using verified local cache at {sha}")
            # Do not overwrite the original fetched_at/head unless the caller wants a fresh remote sync.
            return 0
        print(f"ERROR: remote MCP sync failed and no verified cache is available: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
