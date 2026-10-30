#!/bin/sh
# usage: run_routes.sh <repo-at-head> <outdir> <label>=<set-root> ...
# Runs the head gate on each recorded route set (read-only): the set, reversed, marked, unmarked, record (print).
repo=$1; out=$2; shift 2; mkdir -p "$out"
G="python3 -B $repo/syn/ooc/pp_resource_gate.py"
for pair in "$@"; do
  label=${pair%%=*}; w=${pair#*=}
  S=$w/ax7101/gateware; A=$w/ax7101-AltSpreadLogic_high; E=$w/ax7101-ExtraTimingOpt
  $G check "$S" --endpoint route-1x1 --comparison "$A" --comparison "$E" > "$out/$label-set-check.log" 2>&1; echo "$label-set-check rc=$?" >> "$out/rc.txt"
  $G check "$S" --endpoint route-1x1 --comparison "$E" --comparison "$A" > "$out/$label-set-reversed.log" 2>&1; echo "$label-set-reversed rc=$?" >> "$out/rc.txt"
  $G check "$S" --endpoint route-1x1 --shipping-selection > "$out/$label-marked.log" 2>&1; echo "$label-marked rc=$?" >> "$out/rc.txt"
  $G check "$S" --endpoint route-1x1 > "$out/$label-unmarked.log" 2>&1; echo "$label-unmarked rc=$?" >> "$out/rc.txt"
  $G record "$S" --endpoint route-1x1 --comparison "$A" --comparison "$E" > "$out/$label-set-record.log" 2>&1; echo "$label-set-record rc=$?" >> "$out/rc.txt"
done
