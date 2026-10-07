#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/omaragi-reliability-replay.XXXXXX")"
TARGET="$TEMP_ROOT/reliability_replay"

cleanup() {
  rm -rf "$TEMP_ROOT"
}
trap cleanup EXIT

mkdir -p "$TARGET"
(
  cd "$SOURCE_ROOT"
  tar --exclude='./output' --exclude='*/__pycache__' --exclude='*.pyc' -cf - .
) | (
  cd "$TARGET"
  tar -xf -
)

cd "$TARGET"
./scripts/quickstart.sh --check
test -s output/judge/replay_summary.md
test -s output/judge/report.html
test -s output/judge/report.json
echo "CLEAN_INSTALL_TEST_PASS"
