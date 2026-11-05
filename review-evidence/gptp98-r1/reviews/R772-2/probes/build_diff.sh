#!/bin/sh
# usage: build_diff.sh <hdl-dir> <obj-dir>  (VERILATOR may name the binary)
set -e
HDL=$1; OBJ=$2; HERE=$(cd "$(dirname "$0")" && pwd)
${VERILATOR:-verilator} --cc --exe --build -j 4 --top-module KL_gptp_rx_parser \
  -Wno-fatal -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC --Mdir "$OBJ" \
  -CFLAGS "-std=c++17 -O2" \
  "$HDL/ucpu/gptp_ucpu_pkg.sv" "$HDL/wire/KL_gptp_rx_parser.sv" \
  "$HERE/fu_walk_diff.cpp" -o Vdiff
