#!/bin/sh
# Build and run the reviewer probe against one parser RTL.
# usage: build_probe.sh <hdl-dir> <objdir> <log>
# Needs a Verilator 5.050 first on PATH. Writes <log> and <log>.rc.
set -u
hdl=$1 obj=$2 log=$3
here=$(cd "$(dirname "$0")" && pwd)
rm -rf "$obj"
verilator --cc --exe --build -j 4 --top-module KL_gptp_rx_parser -Wno-fatal \
  -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC --Mdir "$obj" -CFLAGS "-std=c++17 -O1" \
  "$hdl/ucpu/gptp_ucpu_pkg.sv" "$hdl/wire/KL_gptp_rx_parser.sv" \
  "$here/probe_rx_err.cpp" -o Vprobe > "$log.build" 2>&1 || { echo build-failed > "$log"; echo 2 > "$log.rc"; exit 2; }
"$obj/Vprobe" > "$log" 2>&1; echo $? > "$log.rc"
