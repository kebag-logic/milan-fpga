#!/bin/bash
# grp.sh CLONE BUILD POINT VARIANT GROUPS: build (if BUILD has none) and run a few groups of one arm, as the legs do.
set -u
T=<scratch>; . $T/bin/env.sh
export MAKEFLAGS="-j4 --no-print-directory" PYTHONUNBUFFERED=1
C=$1 B=$2 P=$3 V=$4 G=$5
echo "HEAD $(git -C $C rev-parse --short=8 HEAD) dirty $(git -C $C status --porcelain --untracked-files=no | wc -l) $P $V $G start $(date +%T)"
[ -f $B/build.json ] || python3 -B $T/tools/legs.py build $C $B $P $V 1 > $B.build.log 2>&1 || { echo "build rc=$?"; tail -3 $B.build.log; exit 3; }
python3 -B $C/tb/verilator/ctrl_service_budget/run.py --point $P --build-dir $B --reuse-build --out $B/run-$(echo $G | tr ',' '+') --groups $G \
  --record-budget-findings --record-share-findings --jobs 4 $([ $V != none ] && echo --variant $V); echo "END rc=$? $(date +%T)"
