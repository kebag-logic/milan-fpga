#!/usr/bin/env bash
# Build and run the lane's parser suite against an RTL directory, out of tree.
# Usage: suite.sh <hdl-dir> <work-dir> [bench-dir]
set -u
HDL="$1"; W="$2"; BENCH="${3:-$LANES/g35-rx-err/tb/verilator/parser}"
export PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
rm -rf "$W"; mkdir -p "$W"
verilator --cc --exe --build -j 0 --top-module KL_gptp_rx_parser \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
  -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM \
  -CFLAGS "-std=c++17 -O2 -I$BENCH -Wall -Wextra" --Mdir "$W/obj" \
  "$HDL/ucpu/gptp_ucpu_pkg.sv" "$HDL/wire/KL_gptp_rx_parser.sv" \
  "$BENCH/sim_main.cpp" -o Vparser > "$W/build.log" 2>&1
echo "build rc=$?"
"$W/obj/Vparser" > "$W/run.log" 2>&1
echo "run rc=$?"
