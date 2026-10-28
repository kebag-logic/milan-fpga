#!/bin/bash
# One harness leg: leg.sh CHECKOUT BUILD_DIR LOG POINT [run.py args...]; head, elapsed and rc last.
set -u
. "$(dirname "$0")/env.sh"
C=$1 B=$2 L=$3 POINT=$4; shift 4
start=$(date +%s)
{ echo "HEAD $(git -C "$C" rev-parse HEAD 2>/dev/null || echo archive) DIRTY $(git -C "$C" status --porcelain --untracked-files=no 2>/dev/null | wc -l)"
  echo "verilator: $(command -v verilator) $(verilator --version)"
  echo "\$ run.py --point $POINT --build-dir <scratch> --record-budget-findings $*"; } > "$L"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" \
  --record-budget-findings "$@" >> "$L" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s" >> "$L"; echo "rc=$rc" >> "$L"
