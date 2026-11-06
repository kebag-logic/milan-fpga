#!/bin/sh
# run_arm_group.sh <packet> <arm> <group>
P=$1; A=$2; G=$3; L=$P/receipts/mut/$A.top-$G.log
cd "$P/scratch/mut/$A/tb/srp_top"; timeout 400 ./obj_dir/Vsrp_top_sim "$G" > "$L" 2>&1; rc=$?
echo "$A $G rc=$rc $(grep 'checks:' "$L" | tail -1) $(grep '^FAIL' "$L" | cut -c1-70 | head -3 | tr '\n' ';')"
