#!/bin/sh
# Build the reviewer probe harness against one exported tree's parser RTL.
# usage: run_probes.sh TREE OUTDIR LOG
# TREE is an exported FPGA-gPTP tree (git archive), OUTDIR a scratch dir.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
tree=$1; out=$2; log=$3
mkdir -p "$out"
python3 -I "$here/probe_splice.py" "$tree/tb/verilator/parser/sim_main.cpp" \
  "$here/r771_probes.cpp" "$out/probe_main.cpp"
cp "$tree"/tb/verilator/parser/*.h "$out/" 2>/dev/null || true
verilator --cc --exe --build -j 0 --top-module KL_gptp_rx_parser \
  -Wall -Wno-fatal -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-WIDTHEXPAND \
  -Wno-WIDTHTRUNC -Wno-UNUSEDPARAM --Mdir "$out/obj" \
  -CFLAGS "-std=c++17 -O2 -I$tree/tb/verilator/parser -Wall -Wextra" \
  "$tree/hdl/ucpu/gptp_ucpu_pkg.sv" "${RTL:-$tree/hdl/wire/KL_gptp_rx_parser.sv}" \
  "$out/probe_main.cpp" -o Vprobe > "$out/build.log" 2>&1
"$out/obj/Vprobe" > "$log" 2>&1 || true
grep -E 'checks:' "$log"
