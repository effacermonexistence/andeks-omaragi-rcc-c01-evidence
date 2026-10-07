"""Command-line interface for OmarAGI Reliability BYOK Replay."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import load_artifact, run_replay
from .reports import export_reports
from .server import serve_report


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = PROJECT_ROOT / "samples" / "public_demo_replay.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "output" / "judge"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omaragi-replay",
        description=(
            "OmarAGI Reliability BYOK Replay: inspect a sanitized public "
            "decision-path replay artifact."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("run", "serve", "validate"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--input", type=Path, default=DEFAULT_INPUT)
        if command in {"run", "serve"}:
            sub.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
        if command == "serve":
            sub.add_argument("--host", default="127.0.0.1")
            sub.add_argument("--port", type=int, default=8765)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    artifact = load_artifact(args.input)
    if args.command == "validate":
        print(json.dumps({"status": "valid", "cases": len(artifact["cases"])}, indent=2))
        return 0

    report = run_replay(artifact)
    paths = export_reports(report, args.output_dir)
    print(json.dumps({"summary": report["summary"], "outputs": {k: str(v) for k, v in paths.items()}}, indent=2))
    if args.command == "serve":
        serve_report(args.output_dir, args.host, args.port)
    return 0
