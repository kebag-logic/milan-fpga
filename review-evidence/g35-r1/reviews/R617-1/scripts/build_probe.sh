#!/bin/sh
# Build probe_rxerr.cpp against one parser RTL file.
# Usage: build_probe.sh <pkg.sv> <parser.sv> <workdir> ; prints the exe path.
set -eu
PKG=$1; RTL=$2; W=$3
PIN=${PIN:-$VALIDATION_TOOLS/pinned-verilator-5.050}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$W"
"$PIN/verilator" --cc --exe --build -j 4 --top-module KL_gptp_rx_parser \
  -Wno-fatal -Wno-WIDTHEXPAND -Wno-WIDTHTRUNC --Mdir "$W/obj" \
  -CFLAGS "-std=c++17 -O2" "$PKG" "$RTL" "$HERE/probe_rxerr.cpp" -o Vprobe \
  > "$W/build.log" 2>&1
echo "$W/obj/Vprobe"
