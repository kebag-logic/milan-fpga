#!/bin/bash
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683p
export TMPDIR=$T/tmp/np3; mkdir -p $TMPDIR
cd $T/C1b
{ echo "HEAD $(git rev-parse HEAD) DIRTY $(git status --porcelain --untracked-files=no | wc -l)"; python3 -B $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/newplants.py $T/C1b $T/C1b/third_party/lwSRP $T/np3-work step-deadline-read-at-the-end,joint-reset-builds-both,build-turn-ignored; echo "rc=$?"; } > $T/logs/newplants3.log 2>&1
