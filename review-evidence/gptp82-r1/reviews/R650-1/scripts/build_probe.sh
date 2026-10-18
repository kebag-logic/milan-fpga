#!/bin/sh
# usage: build_probe.sh TREE(for RTL+generator) HARNESS_DIR(sim_main.cpp) OUTDIR BINDIR
# Builds the engine harness in HARNESS_DIR against TREE's RTL, generates the
# shipping suite image from TREE's generator, and runs it once.
TREE=$1; H=$2; OUT=$3; export PATH="$4:$PATH"
mkdir -p "$OUT/run"
R=$TREE/hdl
:
verilator --cc --exe --build -j 2 --Mdir "$OUT/obj" --top-module KL_gptp_engine \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
  -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -GUCODE_HEX_P='"gptp_ucode.hex"' \
  -GCLK_HZ_P=2000000 -CFLAGS "-std=c++17 -O2 -I$H -I$TREE/tb/verilator/engine -Wall -Wextra" \
  $R/ucpu/gptp_ucpu_pkg.sv $R/ucpu/KL_gptp_ucpu.sv $R/wire/KL_gptp_rx_parser.sv \
  $R/wire/KL_gptp_tx_slot.sv $R/common/KL_gptp_timer.sv $R/top/KL_gptp_engine.sv \
  "$H/sim_main.cpp" -o Vprobe >"$OUT/build.log" 2>&1 || { echo build failed; exit 2; }
python3 "$TREE/hdl/ucode/gen_gptp_ucode.py" --clk-hz 2000000 --cease-ms 3000 -o "$OUT/run/gptp_ucode.hex" >"$OUT/gen.log" 2>&1 || exit 3
cd "$OUT/run" && ../obj/Vprobe >"$OUT/run.log" 2>&1; echo $? >"$OUT/run.rc"
