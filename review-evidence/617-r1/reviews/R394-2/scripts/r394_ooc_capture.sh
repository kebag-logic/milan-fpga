#!/usr/bin/env bash
# R394-1: the syn/yosys/ooc.sh per-top recipe for KL_chan_map_capture alone
# (sv2v, chparam, synth_xilinx -family xc7 -flatten, stat), run on a given
# source file without ooc.sh's superproject-index/ROM-ledger preamble, which a
# disposable probe copy cannot satisfy. KL_chan_map_capture needs no ROM.
#   r394_ooc_capture.sh <KL_chan_map_capture.sv> <workdir> "<NAME=VALUE ...>"
set -euo pipefail
src="$1"; work="$2"; params="$3"
mkdir -p "$work"
sv2v --top=KL_chan_map_capture "$src" > "$work/cap.v"
chp=""; for kv in $params; do chp="$chp chparam -set ${kv%%=*} ${kv#*=} KL_chan_map_capture;"; done
(cd "$work" && yosys -q -p "read_verilog $work/cap.v;$chp synth_xilinx -family xc7 -top KL_chan_map_capture -flatten; tee -o $work/stat.txt stat")
awk '/Number of cells|LUT[1-6] |FD[CPRSE]+ |RAM[0-9]+[SXM]|RAMB|CARRY4/ {print}' "$work/stat.txt"
