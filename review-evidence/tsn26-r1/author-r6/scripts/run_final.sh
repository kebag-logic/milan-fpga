#!/bin/sh
# usage: run_final.sh TAG SRC
# Runs in SRC itself (a clean clone): validate.py (--jobs 16 --graphs) and baremetal.py (--jobs 8) concurrently.
# Writes S/gates-TAG.pid first and
# S/gates-TAG.done last.
S=<scratch>
L=$2
T=$1
echo $$ > $S/gates-$T.pid
. $S/env.sh
rm -rf $S/val-$T $S/rv32-$T $S/gates-$T.done
cd "$L" || exit 9
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
