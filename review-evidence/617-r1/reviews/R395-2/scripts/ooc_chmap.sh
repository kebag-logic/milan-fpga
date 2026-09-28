#!/usr/bin/env bash
# Reviewer OOC estimate: KL_chan_map_capture alone, sv2v then yosys
# synth_xilinx -family xc7 -flatten (the syn/yosys/ooc.sh synthesis command,
# without its ledger machinery).
# usage: ooc_chmap.sh <sv> <workdir> <N_SLOTS_P> <N_TDM_P> <N_LB_STREAMS_P> <N_LB_CH_P>
set -euo pipefail
src="$1"; w="$2"; mkdir -p "$w"
sv2v --top=KL_chan_map_capture "$src" > "$w/m.v"
yosys -q -p "read_verilog $w/m.v; chparam -set N_SLOTS_P $3 KL_chan_map_capture; \
  chparam -set N_TDM_P $4 KL_chan_map_capture; chparam -set N_LB_STREAMS_P $5 KL_chan_map_capture; \
  chparam -set N_LB_CH_P $6 KL_chan_map_capture; \
  synth_xilinx -family xc7 -flatten -top KL_chan_map_capture; tee -o $w/stat.txt stat" > /dev/null 2>&1
awk '/LUT[1-6]$/ {l+=$1} /FD[RSCP]E$/ {f+=$1} /RAMB|RAM32M|RAM64M/ {r=r" "$2"="$1} END {printf "LUT %d FF %d RAM%s\n", l, f, r}' "$w/stat.txt"
