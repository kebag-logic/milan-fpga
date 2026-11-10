#!/bin/sh
# usage: run_gates.sh CLONE OUT -- the CI's two testing run: steps on a clean clone, concurrently, each with its log, rc
# and time; the clone's head, status and diff hash before and after. Writes OUT/done last.
C=$1 O=$2
. $SCRATCH/env.sh
rm -rf "$O"; mkdir -p "$O"
cd "$C" || exit 9
git rev-parse HEAD > "$O/head"; git status --short > "$O/status-before"; git diff | sha256sum > "$O/diffsha-before"
( /usr/bin/time -v -o "$O/validate.time" python3 scripts/validate.py --work "$O/val" --jobs 16 --graphs > "$O/validate.log" 2>&1; echo $? > "$O/validate.rc" ) &
( /usr/bin/time -v -o "$O/baremetal.time" python3 scripts/baremetal.py --work "$O/rv32" --jobs 16 > "$O/baremetal.log" 2>&1; echo $? > "$O/baremetal.rc" ) &
wait
rm -rf scripts/__pycache__
git status --short > "$O/status-after"; git diff | sha256sum > "$O/diffsha-after"
echo done > "$O/done"
