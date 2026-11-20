#!/bin/bash
# notice.sh IMG CLONE: the attribution experiment's notice path on one image (the manager's resume of 2026-11-20
# 02:3x, "the two notice-path statements ... measured as they now cost"): 8x8/1if's answering-ports arm with its two
# notice groups alone (aecp-fanout, which measures the AECP notice item, and aecp-largest-notice, the long notice), built
# as the full re-measure built it (legs.py build), then three repeats on that build with the formal measurement's
# options, each read by #665 round 28's cost tools (costs_r5.sh).
set -u
T=<scratch>; . $T/bin/env.sh
export MAKEFLAGS="-j4 --no-print-directory" PYTHONUNBUFFERED=1
IMG=$1 C=$2 B=$T/r7attr/notice-$1 G=aecp-fanout,aecp-largest-notice
mkdir -p $B
echo "IMG $IMG HEAD $(git -C $C rev-parse HEAD) dirty $(git -C $C status --porcelain | wc -l) start $(date +%T)"
python3 -B $T/tools/legs.py build $C $B/build 8x8-1if answering-ports 1 $G > $B/build.log 2>&1 \
  || { echo "build rc=$?"; exit 3; }
tail -1 $B/build.log
for k in 1 2 3; do
  ( mkdir -p $B/rep$k
    python3 -B $C/tb/verilator/ctrl_service_budget/run.py --point 8x8-1if --build-dir $B/build --reuse-build \
      --out $B/rep$k/results --groups $G --variant answering-ports \
      --record-budget-findings --record-share-findings --jobs 1 > $B/rep$k.log 2>&1
    echo $? > $B/rep$k.rc
    ln -sf $B/build/build.json $B/rep$k/build.json
    bash $T/tools/survey/costs_r5.sh $T/tools/survey $B/rep$k/costs 8x8/1if 1 $C/tb/verilator/ctrl_service_budget \
      $B/rep$k > $B/rep$k.costs.log 2>&1
    echo "rep $k rc=$(cat $B/rep$k.rc) $(date +%T)" ) &
done
wait
echo "END $(date +%T)"
