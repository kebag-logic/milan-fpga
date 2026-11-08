#!/bin/sh
# usage: run_gates.sh TAG DIR   (runs validate.py and baremetal.py concurrently in DIR)
S=<scratch>
T=$1
D=$2
. $S/env.sh
cd "$D" || exit 9
rm -rf $S/val-$T $S/rv32-$T $S/gates-$T.done
git rev-parse HEAD > $S/gates-$T.head
git status --short > $S/gates-$T.status
git diff | sha256sum > $S/gates-$T.diffsha
( python3 scripts/validate.py --work $S/val-$T --jobs 16 --graphs > $S/val-$T.log 2>&1; echo $? > $S/val-$T.rc ) &
( python3 scripts/baremetal.py --work $S/rv32-$T --jobs 8 > $S/rv32-$T.log 2>&1; echo $? > $S/rv32-$T.rc ) &
wait
git status --short > $S/gates-$T.status-after
git diff | sha256sum > $S/gates-$T.diffsha-after
echo done > $S/gates-$T.done
