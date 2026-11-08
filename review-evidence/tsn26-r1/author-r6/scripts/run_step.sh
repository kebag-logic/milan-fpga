#!/bin/sh
# usage: run_step.sh TAG [SRC]
# Copies SRC (default: the lane working tree, ignored build output excluded) to S/tree-TAG and runs
# validate.py (--jobs 16 --graphs) and baremetal.py (--jobs 8) concurrently there. Writes S/gates-TAG.pid first and
# S/gates-TAG.done last.
S=<scratch>
L=${2:-<lane>}
T=$1
echo $$ > $S/gates-$T.pid
. $S/env.sh
rm -rf $S/tree-$T $S/val-$T $S/rv32-$T $S/gates-$T.done
rsync -a --exclude /build-registration --exclude __pycache__ "$L"/ $S/tree-$T/
cd $S/tree-$T || exit 9
git rev-parse HEAD > $S/gates-$T.head
git status --short > $S/gates-$T.status
git diff | sha256sum > $S/gates-$T.diffsha
( python3 scripts/validate.py --work $S/val-$T --jobs 16 --graphs > $S/val-$T.log 2>&1; echo $? > $S/val-$T.rc ) &
( python3 scripts/baremetal.py --work $S/rv32-$T --jobs 8 > $S/rv32-$T.log 2>&1; echo $? > $S/rv32-$T.rc ) &
wait
rm -rf scripts/__pycache__
git status --short > $S/gates-$T.status-after
git diff | sha256sum > $S/gates-$T.diffsha-after
echo done > $S/gates-$T.done
