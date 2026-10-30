#!/usr/bin/env bash
# Run a gate tree on the three recorded #814 route sets. usage: run_recorded.sh <gate-tree> <out> old|new
# Route roots come from DEV_W, HEAD_W, CTRL_W (each holding ax7101/gateware and the two comparison directories).
set -u
T=$1 O=$2 M=$3; G=$T/syn/ooc/pp_resource_gate.py; mkdir -p "$O"; : > "$O/rc.txt"
run() { local l=$1; shift; local rc=0; python3 -B "$G" "$@" > "$O/$l.log" 2>&1 || rc=$?; echo "$l rc=$rc" >> "$O/rc.txt"; }
for pair in "dev-1e80128f=$DEV_W" "head-8b28ebaf=$HEAD_W" "control-c1=$CTRL_W"; do
  n=${pair%%=*} W=${pair#*=}; S=$W/ax7101/gateware A=$W/ax7101-AltSpreadLogic_high E=$W/ax7101-ExtraTimingOpt
  if [ "$M" = old ]; then
    run $n-EPPO-check check "$S" --endpoint route-1x1 & run $n-ASLH-check check "$A" --endpoint route-1x1 &
    run $n-ETO-check check "$E" --endpoint route-1x1 &
  else
    run $n-set-check check "$S" --endpoint route-1x1 --comparison "$A" --comparison "$E" &
    run $n-set-check-reversed check "$S" --endpoint route-1x1 --comparison "$E" --comparison "$A" &
    run $n-EPPO-marked-check check "$S" --endpoint route-1x1 --shipping-selection &
    run $n-EPPO-unmarked-check check "$S" --endpoint route-1x1 &
    run $n-ASLH-alone-marked check "$A" --endpoint route-1x1 --shipping-selection &
    run $n-set-record record "$S" --endpoint route-1x1 --comparison "$A" --comparison "$E" &
  fi
done
wait; sort "$O/rc.txt"
