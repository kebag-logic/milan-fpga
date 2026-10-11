#!/bin/sh
# Build and run the reviewer rx_err probe against one source tree.
# usage: probe.sh <tree-root> <build-dir>   (VERILATOR may name the binary)
set -eu
root=$1; out=$2
here=$(cd "$(dirname "$0")" && pwd)
V=${VERILATOR:-verilator}
mkdir -p "$out"
"$V" --version
"$V" --cc --exe --build -j 4 --top-module KL_gptp_rx_parser \
  -Wno-fatal -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC -Wno-UNUSEDSIGNAL \
  --Mdir "$out" -CFLAGS "-std=c++17 -O2" \
  "$root/hdl/ucpu/gptp_ucpu_pkg.sv" "$root/hdl/wire/KL_gptp_rx_parser.sv" \
  "$here/probe_rx_err.cpp" -o Vprobe >"$out/build.log" 2>&1
sha256sum "$root/hdl/wire/KL_gptp_rx_parser.sv"
"$out/Vprobe"
