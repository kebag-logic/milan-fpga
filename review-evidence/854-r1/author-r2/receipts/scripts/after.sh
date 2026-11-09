#!/usr/bin/env bash
# after.sh <out>: once the notes are set, check-baseline and check on each endpoint against the new record (in the lane).
set -u
out=$1; S=$VALIDATION_STORAGE/scratch/854-a756b; W=$S/w; W8=$S/w8; LANE=$LANES/854-shadow-drops
cd "$LANE" || exit 2
G="python3 syn/ooc/pp_resource_gate.py"
g() { id=$1; shift; { echo "# $*"; bash -c "$*"; } > "$out/$id.log" 2>&1; echo $? > "$out/$id.rc"; echo "$id rc=$(cat "$out/$id.rc")"; }
g after-check-baseline "$G check-baseline"
g after-route-1x1 "$G check $W/ax7101/gateware --endpoint route-1x1 --comparison $W/ax7101-AltSpreadLogic_high --comparison $W/ax7101-ExtraTimingOpt"
g after-ooc-1x1 "$G check $W/ax7101-ooc --endpoint ooc-1x1"
g after-ooc-8x8 "$G check $W8/ax8x8-ooc --endpoint ooc-8x8"
cp syn/ooc/pp_resource_baseline.json "$out/baseline-final.json"
