#!/usr/bin/env bash
# record_all.sh <out>: the resource gate on the merge commit's three measurements, run in the lane (whose
# syn/ooc/pp_resource_baseline.json it writes). For each endpoint: check against dev 0a75aa77's record (the fourteenth,
# the last one landed: #843's route, #845's standalone records), check against the record the merge carried (round 1's,
# processor 044cb25f on dev 1eb5289d), then record --write. Afterwards check-baseline and check again on each endpoint.
# Every command's whole output goes to <out>/<id>.log and its exit status to <out>/<id>.rc; nothing is piped.
set -u
out=$1; S=$VALIDATION_STORAGE/scratch/851-a744b; W=$S/w; W8=$S/w8; LANE=$LANES/851-pp-pin
mkdir -p "$out"; cd "$LANE" || exit 2
git show 0a75aa774b89ac89351700f63dd8cbb89694af6c:syn/ooc/pp_resource_baseline.json > "$out/baseline-dev-0a75aa77.json"
cp syn/ooc/pp_resource_baseline.json "$out/baseline-merge-e44a4d20.json"
G="python3 syn/ooc/pp_resource_gate.py"
ROUTE="$W/ax7101/gateware --endpoint route-1x1 --comparison $W/ax7101-AltSpreadLogic_high --comparison $W/ax7101-ExtraTimingOpt"
OOC1="$W/ax7101-ooc --endpoint ooc-1x1"
OOC8="$W8/ax8x8-ooc --endpoint ooc-8x8"
g() { id=$1; shift; { echo "# $*"; bash -c "$*"; } > "$out/$id.log" 2>&1; echo $? > "$out/$id.rc"; echo "$id rc=$(cat "$out/$id.rc")"; }
declare -A ARGS=([route-1x1]="$ROUTE" [ooc-1x1]="$OOC1" [ooc-8x8]="$OOC8")
for n in route-1x1 ooc-1x1 ooc-8x8; do
  a=${ARGS[$n]}
  g "check-dev-$n" "$G check $a --baseline $out/baseline-dev-0a75aa77.json"
  g "check-merge-$n" "$G check $a --baseline $out/baseline-merge-e44a4d20.json"
done
for n in route-1x1 ooc-1x1 ooc-8x8; do
  a=${ARGS[$n]}
  g "record-$n" "$G record $a --write"
done
cp syn/ooc/pp_resource_baseline.json "$out/baseline-recorded.json"
