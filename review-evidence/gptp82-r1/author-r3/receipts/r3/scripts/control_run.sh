#!/bin/sh
# Build the head engine harness against another revision's RTL and generator
# and run it with the suite's shipping image arguments, then the fourth pass
# (an image built with --p1 255, +not-gm-capable).
# Usage: control_run.sh <rev> <workdir> <log>
set -e
REV=$1; W=$2; LOG=$3
L=<lane>
rm -rf "$W"; mkdir -p "$W/src" "$W/p1run"
git -C "$L" archive "$REV" hdl | tar -x -C "$W/src"
cd "$W"
python3 src/hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 -o gptp_ucode.hex > gen.log
python3 src/hdl/ucode/gen_gptp_ucode.py --clk-hz 2000000 --cease-ms 3000 --p1 255 -o p1run/gptp_ucode.hex >> gen.log
verilator --cc --exe --build -j 8 --top-module KL_gptp_engine -Wall -Wno-fatal \
  -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -GUCODE_HEX_P='"gptp_ucode.hex"' -GCLK_HZ_P=2000000 \
  -CFLAGS "-std=c++17 -O2 -I$L/tb/verilator/engine" \
  src/hdl/ucpu/gptp_ucpu_pkg.sv src/hdl/ucpu/KL_gptp_ucpu.sv src/hdl/wire/KL_gptp_rx_parser.sv \
  src/hdl/wire/KL_gptp_tx_slot.sv src/hdl/common/KL_gptp_timer.sv src/hdl/top/KL_gptp_engine.sv \
  "$L/tb/verilator/engine/sim_main.cpp" -o Vctl > build.log 2>&1
set +e
./obj_dir/Vctl > "$LOG" 2>&1
echo "rc=$?" >> "$LOG"
echo "-- the fourth pass: --p1 255, +not-gm-capable --" >> "$LOG"
(cd p1run && ../obj_dir/Vctl +not-gm-capable) >> "$LOG" 2>&1
echo "rc=$?" >> "$LOG"
