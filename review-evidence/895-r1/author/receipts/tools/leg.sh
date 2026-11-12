#!/bin/bash
# One or more harness legs in sequence, from the lane's clean clone. usage: leg.sh NAME:POINT:VARIANT[:GROUPS] ...
set -u
T=<scratch>
cd ${CLONE:-$T/L}
rc=0
for spec in "$@"; do
  IFS=: read -r name point variant groups <<< "$spec"
  extra=(); [ "$variant" != "none" ] && extra+=(--variant "$variant"); [ -n "${groups:-}" ] && extra+=(--groups "$groups")
  export TMPDIR=$T/tmp/$name; mkdir -p $TMPDIR
  echo "== $name $(date +%H:%M) point $point variant $variant groups ${groups:-all}"
  PYTHONUNBUFFERED=1 python3 -B tb/verilator/ctrl_service_budget/run.py --point $point --build-dir $T/builds/$name \
     --record-budget-findings --record-share-findings --jobs 7 "${extra[@]}" > $T/legs/$name.log 2>&1
  r=$?; echo "$r" > $T/legs/$name.rc; echo "== $name rc $r $(date +%H:%M)"; [ $r -ne 0 ] && rc=$r
done
exit $rc
