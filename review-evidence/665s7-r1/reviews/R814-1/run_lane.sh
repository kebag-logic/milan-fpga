#!/bin/bash
# run_lane.sh NAME TREE CMD... : run CMD in TREE/tb/verilator/milan_dp with the pinned Verilator; log + rc under receipts/logs
name=$1; tree=$2; shift 2
L=$REVIEWS/665s7-r814-1-packet/receipts/logs
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator VERILATOR_JOBS=${VERILATOR_JOBS:-4}
cd "$tree/tb/verilator/milan_dp" || exit 9
{ echo "# $(date -Is) $name in $tree: $*"; "$@"; rc=$?; echo "# $(date -Is) rc=$rc"; } > "$L/$name.log" 2>&1
echo $rc > "$L/$name.rc"
