#!/bin/bash
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683p
export TMPDIR=$T/tmp/np; mkdir -p $TMPDIR
cd $T/C1
{ echo "HEAD $(git rev-parse HEAD)"; python3 -B $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/newplants.py $T/C1 $T/C1/third_party/lwSRP $T/np-work; echo "rc=$?"; } > $T/logs/newplants.log 2>&1
