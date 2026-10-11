#!/bin/sh
# Reduce the raw Vivado outputs of vivado_runs.sh to path-redacted receipts.
# Usage: extract_vivado.sh <raw-dir> <receipts-dir>
R=$1; OUT=$2
mkdir -p "$OUT"
red() { sed -e 's#/[^ ]*/syn/ooc/#<tree>/syn/ooc/#g' -e 's#/[^ ]*/settings64.sh#<settings64.sh>#g'; }
cp "$R/lock.txt" "$OUT/lock.txt"
for t in head main port; do
  o="$OUT/$t.txt"
  {
    echo "### run: $t   rc=$(cat "$R/run_$t.rc")"
    echo "### gate lines from the run output"
    grep -E "^ooc clock order|^  [a-z_]+\.(log|tcl|xdc)" "$R/run_$t.log" | red
    for top in ucpu engine; do
      L="$R/$t/${top}_ooc.log"; [ -f "$L" ] || continue
      echo "### $top: tool identity"
      grep -m2 -E "^# Vivado v|SW Build" "$L"
      echo "### $top: order lines (log line numbers)"
      grep -n -E "^# read_xdc|^Command: synth_design|^Starting synth_design|^Parsing XDC File|^Start Technology Mapping|^synth_design completed|^# create_clock|^CRITICAL WARNING|^Synthesis finished|Infos, [0-9]+ Warnings" "$L" | red
      U="$R/$t/${top}_util.rpt"; T="$R/$t/${top}_timing.rpt"; H="$R/$t/${top}_util_hier.rpt"
      echo "### $top: utilization ($(grep -m1 -E '^\| Device' "$U" | tr -s ' '))"
      grep -E "^\| (Slice LUTs\*?|  LUT as Logic|  LUT as Memory|Slice Registers|Block RAM Tile|DSPs) " "$U" | tr -s ' '
      grep -E "^\| *u_ucpu " "$H" | tr -s ' '
      echo "### $top: timing"
      grep -A2 "WNS(ns)      TNS(ns)" "$T" | head -3 | tr -s ' '
      grep -m1 -E "checking no_clock" "$T"
      grep -m1 -E "^clk  " "$T" | tr -s ' '
      grep -m1 "^Slack" "$T"
      echo "### $top: report sha256 (body from 'Design Timing Summary' on, paths stripped)"
      sed -n '/Design Timing Summary/,$p' "$T" | red | sha256sum | sed "s#-#${top}_timing body#"
    done
  } > "$o"
done
{ echo "### head log check applied to main's (unconstrained) logs: rc=$(cat "$R/main_logs_under_head_check.rc")"
  red < "$R/main_logs_under_head_check.log"; } > "$OUT/main_logs_under_head_check.txt"
