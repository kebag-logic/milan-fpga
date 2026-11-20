#!/bin/bash
# attr.sh IMG CLONE: the attribution experiment's one image (the manager's resume of 2026-11-20 02:3x): 8x8/1if's
# valid-destinations arm with its srp-talker-held group alone, built as the full re-measure built it (legs.py build,
# run.py's default build: CPU regions cover, the split placement's L1, no XIP), then three repeats of the group at once
# on that build (run.py --reuse-build with the formal measurement's options), each read by #665 round 28's cost tools
# (costs_r5.sh: record.srp and the polls' items, as the survey reads them).
set -u
T=<scratch>; . $T/bin/env.sh
export MAKEFLAGS="-j4 --no-print-directory" PYTHONUNBUFFERED=1
IMG=$1 C=$2 B=$T/r7attr/$1
mkdir -p $B
echo "IMG $IMG HEAD $(git -C $C rev-parse HEAD) dirty $(git -C $C status --porcelain | wc -l) start $(date +%T)"
python3 -B $T/tools/legs.py build $C $B/build 8x8-1if valid-destinations 1 srp-talker-held > $B/build.log 2>&1 \
  || { echo "build rc=$?"; exit 3; }
tail -1 $B/build.log
for k in 1 2 3; do
  ( mkdir -p $B/rep$k
    python3 -B $C/tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir $B/build --reuse-build \
      --out $B/rep$k/results --groups srp-talker-held --variant valid-destinations \
      --record-budget-findings --record-share-findings --jobs 1 > $B/rep$k.log 2>&1
    echo $? > $B/rep$k.rc
    ln -sf $B/build/build.json $B/rep$k/build.json
    bash $T/tools/survey/costs_r5.sh $T/tools/survey $B/rep$k/costs 8x8/1if 1 $C/tb/verilator/ctrl_service_budget \
      $B/rep$k > $B/rep$k.costs.log 2>&1
    echo "rep $k rc=$(cat $B/rep$k.rc) $(date +%T)" ) &
done
wait
echo "END $(date +%T)"
