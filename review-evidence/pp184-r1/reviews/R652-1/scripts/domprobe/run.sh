#!/bin/sh
# Build and run the reviewer's KL_srp_domain bench against a tree.
# usage: run.sh <tree-with-hdl/> <build-dir>
set -eu
TREE=$1; OUT=$2; HERE=$(cd "$(dirname "$0")" && pwd)
VL=${VERILATOR:-verilator}   # Verilator 5.050
mkdir -p "$OUT"
"$VL" --cc --exe --build -j 4 -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL \
  --top-module KL_srp_domain --Mdir "$OUT" \
  "$TREE/hdl/srp/KL_srp_domain.sv" "$HERE/probe.cpp" -o Vprobe >"$OUT/build.log" 2>&1 \
  || { tail -30 "$OUT/build.log"; exit 2; }
"$OUT/Vprobe"
