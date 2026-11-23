#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Disabled-option leaf area, base tree versus head tree: sv2v then a flattened
# xc7 synthesis of KL_render_queue and KL_chan_map_capture with every
# parameter at its default (INPUT_LOOPBACK_P = 0). Prints each stat block.
# Usage: leaf_off.sh <base tree> <head tree> <work dir>
set -euo pipefail
base=$1 head=$2 work=$3
mkdir -p "$work"
for top in KL_render_queue KL_chan_map_capture; do
  for side in base head; do
    tree=$base; [ "$side" = head ] && tree=$head
    d=$work/$side-$top; mkdir -p "$d"
    sv2v -I"$tree/hdl/common" "$tree/hdl/ieee1722/aaf/$top.sv" > "$d/$top.v"
    yosys -q -l "$d/yosys.log" -p "read_verilog $d/$top.v; synth_xilinx -flatten -top $top; tee -o $d/stat.txt stat" > /dev/null
    echo "== $side $top"
    grep -E '^\s+[0-9]+ +(cells|[A-Z0-9_]+$)|Number of cells|LUT|FD|RAMB|CARRY|MUXF' "$d/stat.txt" | sed 's/^ *//' | head -30
  done
  if diff <(grep -vE 'Printing|=== ' "$work/base-$top/stat.txt") <(grep -vE 'Printing|=== ' "$work/head-$top/stat.txt") > /dev/null; then
    echo "LEAF_OFF $top IDENTICAL_STAT"
  else
    echo "LEAF_OFF $top STAT_DIFFERS"
  fi
done
