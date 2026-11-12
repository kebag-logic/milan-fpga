#!/bin/bash
# One part of a harness leg's groups on its existing build, into its own results directory (lane 895 helper).
# usage: part.sh BUILD_NAME POINT PART [VARIANT]   (groups from builds/BUILD_NAME/partPART.groups)
set -u
T=<scratch>
cd ${CLONE:-$T/L}
n=$1 point=$2 part=$3 variant=${4:-none}
extra=(); [ "$variant" != "none" ] && extra+=(--variant "$variant")
export TMPDIR=$T/tmp/$n-p$part; mkdir -p $TMPDIR
echo "== $n part $part $(date +%H:%M) $(git rev-parse --short HEAD)"
PYTHONUNBUFFERED=1 python3 -B tb/verilator/ctrl_service_budget/run.py --point $point --build-dir $T/builds/$n --reuse-build \
  --out $T/builds/$n/results-p$part --groups "$(cat $T/builds/$n/part$part.groups)" \
  --record-budget-findings --record-share-findings --jobs 7 "${extra[@]}" > $T/legs/$n-p$part.log 2>&1
r=$?; echo $r > $T/legs/$n-p$part.rc; echo "== $n part $part rc $r $(date +%H:%M)"
