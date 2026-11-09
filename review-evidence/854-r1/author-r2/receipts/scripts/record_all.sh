#!/usr/bin/env bash
# record_all.sh <out>: the resource gate on the head's three measurements, run in the lane (whose
# syn/ooc/pp_resource_baseline.json it writes). For each endpoint: check against the fifteenth record (the one dev
# ac0a01e3 carries, #851's), then record --write. Afterwards the notes are set by set_measured.py (separately),
# then check-baseline and check again on each endpoint (after.sh). Every command's whole output goes to
# <out>/<id>.log and its exit status to <out>/<id>.rc; nothing is piped.
set -u
out=$1; S=$VALIDATION_STORAGE/scratch/854-a756b; W=$S/w; W8=$S/w8; LANE=$LANES/854-shadow-drops
mkdir -p "$out"; cd "$LANE" || exit 2
git show ac0a01e354d20f5ecac1569c4e7afb3abcbf6f36:syn/ooc/pp_resource_baseline.json > "$out/baseline-dev-ac0a01e3.json"
cmp "$out/baseline-dev-ac0a01e3.json" syn/ooc/pp_resource_baseline.json || { echo "the lane's record is not dev's"; exit 2; }
G="python3 syn/ooc/pp_resource_gate.py"
ROUTE="$W/ax7101/gateware --endpoint route-1x1 --comparison $W/ax7101-AltSpreadLogic_high --comparison $W/ax7101-ExtraTimingOpt"
OOC1="$W/ax7101-ooc --endpoint ooc-1x1"
OOC8="$W8/ax8x8-ooc --endpoint ooc-8x8"
g() { id=$1; shift; { echo "# $*"; bash -c "$*"; } > "$out/$id.log" 2>&1; echo $? > "$out/$id.rc"; echo "$id rc=$(cat "$out/$id.rc")"; }
declare -A ARGS=([route-1x1]="$ROUTE" [ooc-1x1]="$OOC1" [ooc-8x8]="$OOC8")
for n in route-1x1 ooc-1x1 ooc-8x8; do
  g "check-r15-$n" "$G check ${ARGS[$n]} --baseline $out/baseline-dev-ac0a01e3.json"
done
for n in route-1x1 ooc-1x1 ooc-8x8; do
  [ "$(cat "$out/check-r15-$n.rc")" = 0 ] || { echo "check against record 15 failed on $n: no record written"; exit 1; }
done
for n in route-1x1 ooc-1x1 ooc-8x8; do
  g "record-$n" "$G record ${ARGS[$n]} --write"
done
cp syn/ooc/pp_resource_baseline.json "$out/baseline-recorded.json"
