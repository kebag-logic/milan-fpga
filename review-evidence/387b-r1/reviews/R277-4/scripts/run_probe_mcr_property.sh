#!/bin/sh
# R277-4 reviewer probe driver. Builds probe_mcr_property.cpp against the
# committed tkdiag top and a restart engine (default: the tree's own), then
# runs it over seeds and report latencies.
#   usage: run_probe_mcr_property.sh <repo-root> <build-dir> [engine.sv]
# VERILATOR selects the tool (the review used Verilator 5.050).
set -eu
ROOT=$1
BUILD=$2
MCR=${3:-$ROOT/hdl/ieee1722/avtp/KL_media_clock_restart.sv}
HERE=$(cd "$(dirname "$0")" && pwd)
VERILATOR=${VERILATOR:-verilator}
"$VERILATOR" --cc --exe --build -j 8 --top-module tkdiag_tb_top \
  -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
  -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM -Wno-GENUNNAMED \
  -CFLAGS "-std=c++17 -O2" --Mdir "$BUILD" \
  "$ROOT/hdl/ieee1722/avtp/KL_talker_diag_ctx.sv" "$MCR" \
  "$ROOT/tb/verilator/tkdiag/tkdiag_tb_top.sv" "$HERE/probe_mcr_property.cpp" \
  -o Vprobe >/dev/null
rc=0
for lat in 0 1 3; do
  for seed in 1 2 3 4 5 6 7 8 9 10 11 12; do
    if "$BUILD/Vprobe" "$seed" 400000 "$lat" 150 > "$BUILD/last.txt"; then :; else rc=1; fi
    tail -1 "$BUILD/last.txt"
  done
done
exit $rc
