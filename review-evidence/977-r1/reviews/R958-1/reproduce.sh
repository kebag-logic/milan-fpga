#!/usr/bin/env bash
# Run from any directory. ROOT is the detached exact-head checkout, PACKET this directory.
set -euo pipefail
ROOT=${1:?repository path required}
PACKET=${2:?packet path required}
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR="$PACKET/scratch"
mkdir -p "$TMPDIR"
# This driver joins concurrent children before returning; the two mixed probes are expected to return 1.
python3 "$PACKET/run_focused.py" --root "$ROOT" --packet "$PACKET"
python3 "$PACKET/focused_native.py" --root "$ROOT" --packet "$PACKET" --jobs 4
# Optional dependency-complete interpreter supplied by the caller, without modifying its installation.
if [[ -n "${MEMORY_PYTHON:-}" ]]; then
  (cd "$ROOT" && "$MEMORY_PYTHON" sw/litex/test_ctrl_memory.py) > "$PACKET/memory-venv.log" 2>&1
  echo 0 > "$PACKET/memory-venv.rc"
fi
python3 "$PACKET/evidence_audit.py" --root "$ROOT" --packet "$PACKET"
python3 "$PACKET/audit_checkout.py" --root "$ROOT"
