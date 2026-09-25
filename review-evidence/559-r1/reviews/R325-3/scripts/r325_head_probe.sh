#!/bin/sh
# [R325] R325-3 disposable re-measurement of PR #564 at b02af048 (R325-2 probe, head constant only changed) with the head
# harness unchanged: build, simulate and grade one (shape, CPU clock, traffic)
# arm with run.py's own grader. Nothing in the tree is edited; the head's
# explicit --cpu-hz override replaces round 1's yaml edit.
#
# Usage: r325_head_probe.sh <clean clone at b02af048> <scratch dir> <shape> <cpu_hz> <on|off> <captures> <build|sim>
# Environment (the harness README's own prerequisites):
#   LITEX_PY   python3 of the product LiteX environment (patched litex, migen, litedram, litespi, vexii pythondata)
#   SDK_BIN    bin directory of the pinned RV32 SDK (riscv32-linux-gcc)
#   VL_BIN     directory holding the verilator used for the build (identity is recorded)
# The LiteX interpreter's directory precedes the SDK on PATH because the SDK's
# bin also carries a python3 without LiteX; the SDK still supplies every
# riscv32-linux-* tool. The SDK's meson runs `env python3`, so $SCRATCH/shim
# holds only a meson link to the host's (same 1.12.1 release). taskset holds LiteX's make -j<ncpu> to 8 CPUs.
# The build and the simulation are separate foreground steps so each fits a
# bounded wall clock; `sim` runs the native model and grades it.
set -eu
CLONE=$1; SCRATCH=$2; SHAPE=$3; HZ=$4; TRAFFIC=$5; CAP=$6; STEP=$7
HEAD=b02af0480d3a3061df24683d522799d1759f7c33
TREE=$SCRATCH/tree-head
case $SHAPE in *8x8) S=8x8;; *1x1_tdm8) S=1x1;; *) exit 2;; esac
BUILD=$SCRATCH/b${S}_$((HZ / 1000000))_${TRAFFIC}_${CAP}
[ -d "$TREE" ] || cp -a "$CLONE" "$TREE"
test "$(git -C "$TREE" rev-parse HEAD)" = "$HEAD"
test -z "$(git -C "$TREE" status --porcelain --untracked-files=no)"
if [ "$STEP" = build ]; then
  SHIM=$SCRATCH/shim; mkdir -p "$SHIM"; ln -sf "$(command -v meson)" "$SHIM/meson"
  cd "$TREE"
  "$VL_BIN/verilator" --version > "$SCRATCH/$(basename "$BUILD").verilator.txt"
  unshare --user --map-current-user --net env COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true \
    LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 \
    PATH="$SHIM:$(dirname "$LITEX_PY"):$SDK_BIN:$VL_BIN:/usr/bin:/bin" \
    taskset -c 0-7 "$LITEX_PY" -B tb/verilator/nvm_capture_cpu/run.py --shape "$SHAPE" --cpu-hz "$HZ" \
    --traffic "$TRAFFIC" --captures "$CAP" --build-dir "$BUILD" --build-only
  exit 0
fi
cd "$BUILD/gateware"
rc=0; ../native/Vsim > "$BUILD/capture.log" 2>&1 || rc=$?
echo "rc=$rc" > "$BUILD/vsim.rc"
cd "$TREE/tb/verilator/nvm_capture_cpu"
# Grade with the harness's own grader (run.py _grade), unchanged.
"$LITEX_PY" -B -c "
import json, run
from pathlib import Path
b = Path('$BUILD')
run._grade(b, json.loads((b / 'sources.json').read_text()), $rc)
"
