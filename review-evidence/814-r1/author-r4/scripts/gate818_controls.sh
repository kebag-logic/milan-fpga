#!/usr/bin/env bash
# #814 round 4: the #818 gate's controls on the round-4 route set and #818's own self-tests, run in the scratch
# clone at PR #820's head. Receipts redact the scratch root.
# usage: gate818_controls.sh <gate-clone> <work> <receipt-dir>
set -u
G=$1; W=$2; O=$3; S=$VALIDATION_STORAGE/scratch/814-a703d
cd "$G" || exit 2
run() {
  name=$1; shift
  python3 -B "$@" > "$O/$name.raw" 2>&1
  echo $? > "$O/$name.rc"
  sed "s#$S#<scratch>#g" "$O/$name.raw" > "$O/$name.log"
  rm "$O/$name.raw"
  echo "$name rc $(cat "$O/$name.rc")"
}
run check-shipping-alone syn/ooc/pp_resource_gate.py check "$W/ax7101/gateware" --endpoint route-1x1 --shipping-selection
run control-no-set syn/ooc/pp_resource_gate.py check "$W/ax7101/gateware" --endpoint route-1x1
run control-eto-alone syn/ooc/pp_resource_gate.py check "$W/ax7101-ExtraTimingOpt" --endpoint route-1x1 --shipping-selection
: > "$O/selftests.txt"
for t in builtin set_selftest selftest mutants; do
  case $t in
    builtin) args=(syn/ooc/pp_resource_gate.py --selftest) ;;
    *) args=("syn/ooc/pp_resource_gate_$t.py") ;;
  esac
  s=$(date +%s)
  python3 -B "${args[@]}" > "$O/pp_resource_gate_$t.log" 2>&1
  echo "$? $(( $(date +%s) - s ))s ${args[*]}" >> "$O/selftests.txt"
done
git rev-parse HEAD > "$O/gate-head.txt"
git status --short > "$O/gate-status.txt"
