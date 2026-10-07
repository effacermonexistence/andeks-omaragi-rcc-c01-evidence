#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export PYTHONPATH="$ROOT"
python3 scripts/public_safety_scan.py
python3 -m unittest discover -s tests -v
python3 -m omaragi_reliability_replay validate --input samples/public_demo_replay.json
python3 -m omaragi_reliability_replay run \
  --input samples/public_demo_replay.json \
  --output-dir output/smoke

test -s output/smoke/report.json
test -s output/smoke/report.html
test -s output/smoke/replay_summary.md
echo "SMOKE_TEST_PASS"
