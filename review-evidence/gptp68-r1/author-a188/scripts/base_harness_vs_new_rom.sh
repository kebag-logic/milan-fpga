#!/bin/sh
# Build the BASE engine harness (sim_main.cpp at the base commit) against the
# unchanged RTL and run it on the NEW shipping engine image. Its failures are
# exactly the pre-existing checks that encoded the retired rule ("step every
# pair whose |offset| exceeds 20 us"). Nonzero exit is the EXPECTED outcome.
set -u
. $REVIEWS/gptp68-a188-packet/scripts/env.sh
BASE=${BASE:-c1b617435824929a790739ea8585c3fe1a328cc0}
cd "$A188_LANE/tb/verilator/engine" || exit 2
T=$(mktemp -d)
git show "$BASE:tb/verilator/engine/sim_main.cpp" > "$T/sim_main.cpp"
python3 ../../../hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o "$T/gptp_ucode.hex" >/dev/null
verilator --cc --exe --build -j 8 --top-module KL_gptp_engine -Wall -Wno-fatal \
  -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
  -CFLAGS "-std=c++17 -O2 -I$PWD -Wall -Wextra" --Mdir "$T/obj" \
  ../../../hdl/ucpu/gptp_ucpu_pkg.sv ../../../hdl/ucpu/KL_gptp_ucpu.sv \
  ../../../hdl/wire/KL_gptp_rx_parser.sv ../../../hdl/wire/KL_gptp_tx_slot.sv \
  ../../../hdl/common/KL_gptp_timer.sv ../../../hdl/top/KL_gptp_engine.sv \
  "$T/sim_main.cpp" -o Vbase >"$T/build.log" 2>&1 || { echo "build failed"; tail "$T/build.log"; exit 2; }
cd "$T" && ./obj/Vbase > run.log 2>&1
rc=$?
grep -E '^FAIL|checks:' run.log
echo "base harness on new ROM: exit $rc (nonzero expected)"
rm -rf "$T"
exit $rc
