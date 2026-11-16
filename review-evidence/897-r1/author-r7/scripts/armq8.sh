#!/bin/bash
# One quarter of the full arm A at 8x8/2if (round 7; armq.sh at 8x8) (#894 round 13's armA.sh): part 1 builds into BUILD and runs its groups into
# BUILD/results-q1; the others wait for that build, then reuse it for their groups into BUILD/results-qN.
# usage: armq.sh PART CLONE BUILD
set -u
P=$1 C=$2 B=$3 W=/data-2/milan/tmp/897-a776
. $W/scripts/env.sh
export TMPDIR=$W/r4/tmp/armq-$P MAKEFLAGS="-j8 --no-print-directory" PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR"
G=$(cat $W/r4/groups/armA8-q$P.groups)
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) part $P start $(date +%T)"
if [ "$P" = 1 ]; then
  rm -rf "$B"; mkdir -p "$B"
  python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point 8x8 --build-dir "$B" --groups "$G" \
      --out "$B/results-q1" --record-budget-findings --record-share-findings --jobs 8
else
  timeout 3600 bash -c "until [ -s '$B/build.json' ] && [ -e '$B/native/Vsim' ] && [ -e '$B/results-q1' ]; do sleep 20; done" || { echo "no build"; exit 3; }
  python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point 8x8 --build-dir "$B" --reuse-build --groups "$G" \
      --out "$B/results-q$P" --record-budget-findings --record-share-findings --jobs 8
fi
rc=$?; echo "rc=$rc end $(date +%T)"; exit $rc
