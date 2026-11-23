#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Disabled-option leaf area as milan_datapath sees it: the head's new #979
# ports are stripped of port status before synthesis (inputs tied to zero,
# outputs left unread, which is what the disabled render queue does with
# them), so only logic that survives in context is counted. Base and head are
# synthesised identically (flattened xc7, all parameters default). The
# comparison excludes IBUF/OBUF, which only count ports.
# Usage: leaf_off_incontext.sh <base tree> <head tree> <work dir>
set -euo pipefail
base=$1 head=$2 work=$3
mkdir -p "$work"
declare -A strip
strip[KL_chan_map_capture]="input_capture_o input_read_o input_addr_o input_sample_i"
strip[KL_render_queue]="input_map_i input_invalidate_i input_capture_i input_read_i input_addr_i input_capture_ns_i input_sample_o"
for top in KL_chan_map_capture KL_render_queue; do
  for side in base head; do
    tree=$base; [ "$side" = head ] && tree=$head
    d=$work/$side-$top; mkdir -p "$d"
    sv2v -I"$tree/hdl/common" "$tree/hdl/ieee1722/aaf/$top.sv" > "$d/$top.v"
    sel=""
    if [ "$side" = head ]; then for w in ${strip[$top]}; do sel="$sel $top/$w"; done; fi
    # Ports lose their port status after mapping (an earlier delete trips a
    # memory assertion in this synthesiser); the cleanup then removes every
    # cell whose only reader was a stripped output, and folds tied inputs.
    cmd="read_verilog $d/$top.v; synth_xilinx -flatten -top $top;"
    [ -n "$sel" ] && cmd="$cmd delete -port $sel; setundef -zero -undriven; opt_lut; opt -full; opt_clean -purge;"
    [ -z "$sel" ] && cmd="$cmd opt_lut; opt -full; opt_clean -purge;"
    cmd="$cmd tee -o $d/stat.txt stat"
    yosys -q -l "$d/yosys.log" -p "$cmd" > /dev/null
    awk '/^ +[0-9]+ +[A-Z][A-Z0-9_]*$/ && $2 !~ /^(IBUF|OBUF)$/ {print $2, $1}' "$d/stat.txt" | sort > "$d/cells.txt"
  done
  echo "== $top (cell: base head delta)"
  join -a1 -a2 -e 0 -o 0,1.2,2.2 "$work/base-$top/cells.txt" "$work/head-$top/cells.txt" \
    | awk '{d=$3-$2; printf "%-10s %7d %7d %+6d\n", $1, $2, $3, d; if ($1 ~ /^LUT/) {lb+=$2; lh+=$3} if ($1 ~ /^FD/) {fb+=$2; fh+=$3}}
           END {printf "%-10s %7d %7d %+6d\n%-10s %7d %7d %+6d\n", "LUT(all)", lb, lh, lh-lb, "FF(all)", fb, fh, fh-fb}'
done
