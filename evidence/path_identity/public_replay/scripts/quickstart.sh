#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export PYTHONPATH="$ROOT"
HOST="${OMARAGI_REPLAY_HOST:-127.0.0.1}"
PORT="${OMARAGI_REPLAY_PORT:-8765}"

./scripts/smoke_test.sh
python3 -m omaragi_reliability_replay run \
  --input samples/public_demo_replay.json \
  --output-dir output/judge

if [[ "${1:-}" == "--check" ]]; then
  echo "QUICKSTART_CHECK_PASS"
  exit 0
fi

python3 -m omaragi_reliability_replay serve \
  --input samples/public_demo_replay.json \
  --output-dir output/judge \
  --host "$HOST" \
  --port "$PORT"
