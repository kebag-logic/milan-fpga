#!/usr/bin/env bash
# Reviewer reproduction of one capture arm at the exact head, split into
# build and native-run steps so each stays inside a foreground time budget.
# Usage: repro_capture.sh build|run|grade <shape> <cpu_hz> <traffic> <build_dir>
# Environment: PRODUCT_PYTHON (product LiteX interpreter), SDK_BIN (RV32 SDK bin),
# REPO (exact-head checkout). Network is disabled with an unprivileged namespace.
set -euo pipefail
step=$1 shape=$2 hz=$3 traffic=$4 bdir=$5
cd "$REPO"
export PATH="$SDK_BIN:$(dirname "$PRODUCT_PYTHON"):/usr/local/bin:/usr/bin:/bin"
export PYTHON="$PRODUCT_PYTHON" LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0
export COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
case $step in
  build)
    exec unshare -Urn "$PRODUCT_PYTHON" -B tb/verilator/nvm_capture_cpu/run.py \
      --shape "$shape" --cpu-hz "$hz" --captures 16 --traffic "$traffic" \
      --build-dir "$bdir" --build-only ;;
  run)
    cd "$bdir/gateware"
    set +e
    unshare -Urn "$bdir/native/Vsim" > "$bdir/capture.log" 2>&1
    echo "VSIM_RC=$?" > "$bdir/vsim_rc.txt"
    cat "$bdir/vsim_rc.txt" ;;
  grade)
    rc=$(sed -n 's/^VSIM_RC=//p' "$bdir/vsim_rc.txt")
    exec "$PRODUCT_PYTHON" -B -c '
import json, sys
from pathlib import Path
sys.path.insert(0, "tb/verilator/nvm_capture_cpu")
import run
b = Path(sys.argv[1])
spec = json.loads((b / "sources.json").read_text())
run._grade(b, spec, int(sys.argv[2]))
' "$bdir" "$rc" ;;
esac
