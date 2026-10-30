#!/bin/sh
# usage: run_routes.sh <gate-tree> <outdir>
# Runs one gate tree read-only on the recorded route sets: the set, reversed, marked, unmarked, and record (print).
# A set given as label=<shipping dir>,<AltSpreadLogic_high dir>,<ExtraTimingOpt dir>; a lone route as label=<dir>.
# Absolute storage paths are rewritten to <label> placeholders in the logs.
tree=$1; out=$2; mkdir -p "$out"; : > "$out/rc.txt"
G="python3 -B $tree/syn/ooc/pp_resource_gate.py"
R=${VALIDATION_STORAGE:?set VALIDATION_STORAGE to the storage root holding scratch/}/scratch
SETS="dev-1e80128f=$R/814-a703/viv-dev/w1/ax7101/gateware,$R/814-a703/viv-dev/w1/ax7101-AltSpreadLogic_high,$R/814-a703/viv-dev/w1/ax7101-ExtraTimingOpt
h1-8b28ebaf=$R/814-a703b/w-h1/ax7101/gateware,$R/814-a703b/w-h1/ax7101-AltSpreadLogic_high,$R/814-a703b/w-h1/ax7101-ExtraTimingOpt
c1-814-control=$R/814-a703b/w-c1/ax7101/gateware,$R/814-a703b/w-c1/ax7101-AltSpreadLogic_high,$R/814-a703b/w-c1/ax7101-ExtraTimingOpt
pr806=$R/806-a701/viv-cf3ef596/w1/ax7101/gateware,$R/806-a701b/ax7101-AltSpreadLogic_high,$R/806-a701b/ax7101-ExtraTimingOpt
pr787=$R/787-a700/viv-head-a0e555a7/w1/ax7101/gateware,$R/787-a700/viv-head-a0e555a7/w1/ax7101-AltSpreadLogic_high,$R/787-a700/viv-head-a0e555a7/w1/ax7101-ExtraTimingOpt
pr817=$R/817-a709/w-h1/ax7101/gateware"
run() { lab=$1; shift; $G "$@" > "$out/$lab.raw" 2>&1; rc=$?
  sed "s#$R/[^ ]*/ax7101#<route>/ax7101#g" "$out/$lab.raw" > "$out/$lab.log"; rm -f "$out/$lab.raw"
  echo "$lab rc=$rc" >> "$out/rc.txt"; }
echo "$SETS" | while IFS= read -r pair; do
  label=${pair%%=*}; dirs=${pair#*=}
  S=${dirs%%,*}; rest=${dirs#*,}
  if [ "$rest" != "$dirs" ]; then
    A=${rest%%,*}; E=${rest#*,}
    run "$label-set-check" check "$S" --endpoint route-1x1 --comparison "$A" --comparison "$E"
    run "$label-set-reversed" check "$S" --endpoint route-1x1 --comparison "$E" --comparison "$A"
    run "$label-set-record" record "$S" --endpoint route-1x1 --comparison "$A" --comparison "$E"
  fi
  run "$label-marked" check "$S" --endpoint route-1x1 --shipping-selection
  run "$label-unmarked" check "$S" --endpoint route-1x1
  run "$label-marked-record" record "$S" --endpoint route-1x1 --shipping-selection
done
