#!/usr/bin/env bash
# Run one gate tree on the recorded route sets (#814 dev/head/control, #806, #787, #817), one log and rc per run.
# usage: recorded_sets.sh <gate-tree> <out>
# Set roots are under $ROUTES (default $VALIDATION_STORAGE/scratch). #806's comparisons live beside, not under, its shipping
# route; #817 recorded its shipping route only, so it is judged marked.
set -u
T=$1 O=$2 R=${ROUTES:-$VALIDATION_STORAGE/scratch}; G=$T/syn/ooc/pp_resource_gate.py; mkdir -p "$O"; : > "$O/rc.txt"
run() { while [ "$(jobs -rp | wc -l)" -ge "${JOBS:-6}" ]; do wait -n; done; local l=$1; shift; ( local rc=0; python3 -B "$G" "$@" > "$O/$l.log" 2>&1 || rc=$?; echo "$l rc=$rc" >> "$O/rc.txt" ) & }
declare -A SHIP=([dev-1e80128f]=$R/814-a703/viv-dev/w1 [head-8b28ebaf]=$R/814-a703b/w-h1 [control-c1]=$R/814-a703b/w-c1
                 [pr806-cf3ef596]=$R/806-a701/viv-cf3ef596/w1 [pr787-a0e555a7]=$R/787-a700/viv-head-a0e555a7/w1)
declare -A COMP=([pr806-cf3ef596]=$R/806-a701b)
for n in dev-1e80128f head-8b28ebaf control-c1 pr806-cf3ef596 pr787-a0e555a7; do
  W=${SHIP[$n]} C=${COMP[$n]:-${SHIP[$n]}}; S=$W/ax7101/gateware A=$C/ax7101-AltSpreadLogic_high E=$C/ax7101-ExtraTimingOpt
  run $n-set-check check "$S" --endpoint route-1x1 --comparison "$A" --comparison "$E"
  run $n-set-check-reversed check "$S" --endpoint route-1x1 --comparison "$E" --comparison "$A"
  run $n-EPPO-marked-check check "$S" --endpoint route-1x1 --shipping-selection
  run $n-EPPO-unmarked-check check "$S" --endpoint route-1x1
  run $n-set-record record "$S" --endpoint route-1x1 --comparison "$A" --comparison "$E"
done
S=$R/817-a709/w-h1/ax7101/gateware
run pr817-EPPO-marked-check check "$S" --endpoint route-1x1 --shipping-selection
run pr817-EPPO-unmarked-check check "$S" --endpoint route-1x1
run pr817-EPPO-marked-record record "$S" --endpoint route-1x1 --shipping-selection
wait; sort -o "$O/rc.txt" "$O/rc.txt"; cat "$O/rc.txt"
