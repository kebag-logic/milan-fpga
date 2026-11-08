#!/bin/sh
# usage: run_gates.sh TAG   (runs in the clean clone)
S=$VALIDATION_STORAGE/tsn26-a750c
T=$1
. $S/env.sh
cd $S/clone || exit 9
rm -rf $S/val-$T $S/rv32-$T
git rev-parse HEAD > $S/gates-$T.head
git status --short > $S/gates-$T.status
( python3 scripts/validate.py --work $S/val-$T --jobs 16 --graphs > $S/val-$T.log 2>&1; echo $? > $S/val-$T.rc ) &
( python3 scripts/baremetal.py --work $S/rv32-$T --jobs 8 > $S/rv32-$T.log 2>&1; echo $? > $S/rv32-$T.rc ) &
wait
git status --short > $S/gates-$T.status-after
echo done > $S/gates-$T.done
