#!/bin/sh
# [R325] disposable probe for PR #564 at 32076148: measure the 8x8 capture copy
# with the harness unchanged, at the configured 100 MHz CPU clock and at the
# 50 MHz CPU clock of the bare-metal build contract, with and without traffic.
#
# Usage: r325_clock_probe.sh <clean clone at 32076148> <scratch dir> <cpu_mhz 50|100> <none|no-traffic> <captures>
# Environment (the harness README's own prerequisites):
#   LITEX_PY   python3 of the product LiteX environment (litex, migen, litedram, litespi, vexii pythondata)
#   SDK_BIN    bin directory of the pinned RV32 SDK (riscv32-linux-gcc)
# Every step runs in the foreground; the simulator is run separately so each
# step fits a bounded wall clock.
set -eu
CLONE=$1; SCRATCH=$2; MHZ=$3; MUT=$4; CAP=$5
TREE=$SCRATCH/tree$MHZ
BUILD=$SCRATCH/b8x8_${MHZ}_${MUT}
[ -d "$TREE" ] || cp -a "$CLONE" "$TREE"
test "$(git -C "$TREE" rev-parse HEAD)" = 32076148acb0b9122e8c92a44f8e2ebbc8169280
if [ "$MHZ" = 50 ]; then
  # The only change: the 8x8 CPU (milan) clock set to the build-contract 50 MHz.
  sed -i 's/^    milan_clk_hz: 100000000          # single fast domain (AX timing CLOSED)$/    milan_clk_hz: 50000000           # R325 PROBE: build-contract CPU clock/' \
    "$TREE/configs/endstation_ax7101_8x8.yaml"
  grep -q 'milan_clk_hz: 50000000 ' "$TREE/configs/endstation_ax7101_8x8.yaml"
fi
cd "$TREE"
unshare --user --map-current-user --net env COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true \
  LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 PATH="$SDK_BIN:$(dirname "$LITEX_PY"):/usr/bin:/bin" \
  "$LITEX_PY" tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 \
  --captures "$CAP" --mutation "$MUT" --build-dir "$BUILD" --build-only
cd "$BUILD/gateware"
rc=0; ../native/Vsim > "$BUILD/capture.log" 2>&1 || rc=$?
echo "rc=$rc" > "$BUILD/vsim.rc"
cd "$TREE"
# Grade with the harness's own grader (run.py _grade), unchanged.
"$LITEX_PY" -B -c "
import json, sys
sys.path.insert(0, 'tb/verilator/nvm_capture_cpu')
import run
from pathlib import Path
b = Path('$BUILD')
run._grade(b, json.loads((b / 'sources.json').read_text()), $rc)
"
