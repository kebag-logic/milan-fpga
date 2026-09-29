#!/bin/sh
# Builder bank test on the composed candidate, with the pinned RV32 SDK from
# <packet>/scratch/home (HOME is pointed there so Path.home() finds it).
# Usage: run_builder.sh <repo> <packet> <python> <verilator-bin-dir> [litex-python] [tag]
# With [litex-python] set, MILAN_LITEX_PYTHON points at it for the elaboration
# arms, and PYTHONDONTWRITEBYTECODE=1 keeps bytecode out of that install.
set -u
REPO=$1; PK=$2; PY=$3; VBIN=$4; LPY=${5:-}; TAG=${6:-}
cd "$REPO" || exit 2
log=$PK/receipts/builder_test${TAG}.log
{
  echo "\$ HOME=<packet>/scratch/home ${LPY:+MILAN_LITEX_PYTHON=$LPY PYTHONDONTWRITEBYTECODE=1 }taskset -c 0-7 $PY -u sw/builder/test_builder.py --require-rv32 --require-elaboration"
  echo "head: $(git rev-parse HEAD) tree: $(git rev-parse 'HEAD^{tree}')"
  echo "verilator: $(PATH=$VBIN:$PATH verilator --version)"
  echo "sdk: $("$PK/scratch<home-path>/host/bin/riscv32-linux-gcc" --version | head -1)"
  echo "start: $(date -u +%FT%TZ)"
} > "$log"
t0=$(date +%s)
if [ -n "$LPY" ]; then export MILAN_LITEX_PYTHON="$LPY" PYTHONDONTWRITEBYTECODE=1; fi
HOME=$PK/scratch/home PATH=$VBIN:$PATH taskset -c 0-7 timeout 5400 "$PY" -u sw/builder/test_builder.py --require-rv32 --require-elaboration >> "$log" 2>&1
rc=$?
echo "end: $(date -u +%FT%TZ) wall_s=$(( $(date +%s) - t0 )) rc=$rc" >> "$log"
echo "builder_test${TAG} rc=$rc" > "$PK/receipts/builder_test${TAG}_rc.txt"
