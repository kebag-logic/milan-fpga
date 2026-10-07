#!/usr/bin/env bash
# usage: bound_probe_one.sh PACKET REPO NAME PATH OLD NEW
# Plants one SRP bound understatement and runs srp_app.cpp and test_acmp_mbx.cpp at IF=1 and IF=2.
set -u
P=$1; R=$2; name=$3; rel=$4; old=$5; new=$6
src=$P/scratch/plants/$name/ctrl
python3 -I $P/scripts/plant.py "$R/sw/firmware/ctrl" "$src" "$rel" "$old" "$new" > $P/receipts/bounds/$name.plant.log 2>&1 || { echo "plant-refused" > $P/receipts/bounds/$name.rc; exit 0; }
summary=""
for suite in srp_app.cpp test_acmp_mbx.cpp; do
  for i in 1 2; do
    log=$P/receipts/bounds/$name.${suite%.cpp}.if$i.log
    python3 $P/scripts/run_arm.py "$R" "$P/scratch/lwSRP" "$P/scratch/plants/$name/out-${suite%.cpp}-if$i" "$suite" '*' "$i" "$src" > "$log" 2>&1
    summary="$summary ${suite%.cpp}.if$i=$?"
  done
done
echo "$summary" > $P/receipts/bounds/$name.rc
