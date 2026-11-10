#!/bin/sh
# usage: run_step.sh TAG SRC [copy]
# With "copy", SRC's working tree is copied to tree-TAG first (build output excluded); otherwise SRC is a clean clone and
# runs in place. Then validate.py (--jobs 8 --graphs) and baremetal.py (--jobs 8) run concurrently, each with its log and rc;
# the tree's head, status and diff hash are kept before and after. Writes gates-TAG.done last.
S=$SCRATCH/donor
T=$1 L=$2
. $S/env.sh
rm -rf $S/val-$T $S/rv32-$T $S/gates-$T.done
if [ "${3:-}" = copy ]; then rm -rf $S/tree-$T; rsync -a --exclude __pycache__ "$L"/ $S/tree-$T/; L=$S/tree-$T; fi
cd "$L" || exit 9
git rev-parse HEAD > $S/gates-$T.head
git status --short > $S/gates-$T.status
git diff | sha256sum > $S/gates-$T.diffsha
( /usr/bin/time -v -o $S/val-$T.time python3 scripts/validate.py --work $S/val-$T --jobs 8 --graphs > $S/val-$T.log 2>&1; echo $? > $S/val-$T.rc ) &
( /usr/bin/time -v -o $S/rv32-$T.time python3 scripts/baremetal.py --work $S/rv32-$T --jobs 8 > $S/rv32-$T.log 2>&1; echo $? > $S/rv32-$T.rc ) &
wait
rm -rf scripts/__pycache__
git status --short > $S/gates-$T.status-after
git diff | sha256sum > $S/gates-$T.diffsha-after
echo done > $S/gates-$T.done
