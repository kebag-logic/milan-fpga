#!/usr/bin/env bash
# Reviewer OOC estimate: KL_chan_map_capture alone at the 1x1 TDM8 parameters,
# sv2v then yosys synth_xilinx -family xc7 -flatten (the syn/yosys/ooc.sh
# synthesis command, without its ledger machinery). usage: ooc_chmap.sh <sv> <workdir>
set -euo pipefail
src="$1"; w="$2"; mkdir -p "$w"
sv2v --top=KL_chan_map_capture "$src" > "$w/m.v"
yosys -q -p "read_verilog $w/m.v; chparam -set N_SLOTS_P 4 KL_chan_map_capture; \
  chparam -set N_TDM_P 8 KL_chan_map_capture; chparam -set N_LB_STREAMS_P 1 KL_chan_map_capture; \
  chparam -set N_LB_CH_P 8 KL_chan_map_capture; \
  synth_xilinx -family xc7 -flatten -top KL_chan_map_capture; tee -o $w/stat.txt stat" > /dev/null
grep -E "LUT[1-6]|FD[RSCP]E|RAM|Number of cells|cells$" "$w/stat.txt"
