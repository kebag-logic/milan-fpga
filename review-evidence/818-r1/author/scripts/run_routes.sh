#!/usr/bin/env bash
# #818: run one gate tree's check on the recorded routes, one log and rc per run, outputs in <out>.
# usage: run_routes.sh <gate-tree> <out> <mode>   mode: old (each directory alone) | new (sets and marked routes)
set -u
TREE=$1 OUT=$2 MODE=$3
GATE="$TREE/syn/ooc/pp_resource_gate.py"
mkdir -p "$OUT"
declare -A SETS=([dev-1e80128f]=$VALIDATION_STORAGE/scratch/814-a703/viv-dev/w1
                 [head-8b28ebaf]=$VALIDATION_STORAGE/scratch/814-a703b/w-h1
                 [control-c1]=$VALIDATION_STORAGE/scratch/814-a703b/w-c1)
run() {  # <label> <args...>
  local label=$1; shift
  local rc=0
  python3 -B "$GATE" "$@" > "$OUT/$label.log" 2>&1 || rc=$?
  echo "$label rc=$rc" | tee -a "$OUT/rc.txt"
}
for name in dev-1e80128f head-8b28ebaf control-c1; do
  W=${SETS[$name]}
  S=$W/ax7101/gateware A=$W/ax7101-AltSpreadLogic_high E=$W/ax7101-ExtraTimingOpt
  if [ "$MODE" = old ]; then
    run "$name-EPPO-check" check "$S" --endpoint route-1x1
    run "$name-ASLH-check" check "$A" --endpoint route-1x1
    run "$name-ETO-check" check "$E" --endpoint route-1x1
  else
    run "$name-set-check" check "$S" --endpoint route-1x1 --comparison "$A" --comparison "$E"
    run "$name-set-check-reversed" check "$S" --endpoint route-1x1 --comparison "$E" --comparison "$A"
    run "$name-EPPO-marked-check" check "$S" --endpoint route-1x1 --shipping-selection
    run "$name-EPPO-unmarked-check" check "$S" --endpoint route-1x1
    run "$name-set-record" record "$S" --endpoint route-1x1 --comparison "$A" --comparison "$E"
  fi
done
