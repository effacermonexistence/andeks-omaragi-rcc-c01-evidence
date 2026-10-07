#!/usr/bin/env python3
"""Fail closed on obvious secret, local-path, branding, or private-source leakage."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEXT_NAMES = {"LICENSE", ".gitignore"}
TEXT_SUFFIXES = {".py", ".json", ".md", ".sh", ".toml", ".txt"}
SKIP_PARTS = {".git", ".omc", ".venv", "__pycache__", "output", "build", "dist"}

SECRET_PATTERNS = {
    "OpenAI-style secret": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "non-empty secret assignment": re.compile(
        r"(?im)^[A-Z0-9_]*(?:SECRET|PASSWORD|API_KEY|PRIVATE_KEY|ACCESS_TOKEN)"
        r"[A-Z0-9_]*=(?!\s*$).+$"
    ),
}

# Construct forbidden strings so this scanner does not trigger on its own source.
FORBIDDEN_TEXT = {
    "local user path": "/" + "Users" + "/",
    "private Codex path": "." + "codex" + "/",
    "wrong brand no-space variant": "Omar" + "AI",
    "wrong brand spaced variant": "Omar" + " AI",
    "wrong domain": "omar" + "ai.ai.com",
    "private partner name": "Neo" + "Mundi",
}

REQUIRED_FILES = {
    "README.md",
    "BUILD_WEEK.md",
    "EVIDENCE.md",
    "PUBLIC_LOGIC_BOUNDARY.md",
    "LICENSE",
    ".gitignore",
    "pyproject.toml",
    "samples/public_demo_replay.json",
    "examples/example_report.json",
}


def iter_text_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(
            part in SKIP_PARTS or part.endswith(".egg-info") for part in path.parts
        ):
            continue
        if path.suffix in TEXT_SUFFIXES or path.name in TEXT_NAMES:
            files.append(path)
    return sorted(files)


def main() -> int:
    failures: list[str] = []
    for required in sorted(REQUIRED_FILES):
        if not (ROOT / required).is_file():
            failures.append(f"missing required public file: {required}")

    files = iter_text_files()
    for path in files:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{relative}: {label}")
        for label, value in FORBIDDEN_TEXT.items():
            if value.casefold() in text.casefold():
                failures.append(f"{relative}: {label}")

    sample_path = ROOT / "samples" / "public_demo_replay.json"
    if sample_path.is_file():
        sample = json.loads(sample_path.read_text(encoding="utf-8"))
        if sample.get("synthetic") is not True or sample.get("public_only") is not True:
            failures.append("sample is not explicitly synthetic and public_only")

    if failures:
        print("PUBLIC_SAFETY_SCAN_FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"PUBLIC_SAFETY_SCAN_PASS files={len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
