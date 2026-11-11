#!/bin/bash
# chainX: the wire-timing self-test and git diff --check against the merge base, on a fresh clone of the gate head
set -u
S=<scratch>; G=$S/gates4; H=$(cat $G/HEAD); W=$G/extra/wt; L=$G/extra/logs
bash $S/clone_at.sh $H $W > $L/clone.log 2>&1 || exit 3
cd $W || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
run() { id=$1; shift; { echo "# head $H gate $id: $*"; PYTHONHASHSEED=0 taskset -c 68-71 bash -c "$*"; } > "$L/$id.log" 2>&1; rc=$?; echo $rc > "$L/$id.rc"; echo "$id rc=$rc" >> $G/extra/jobs.txt; }
run wire-self-test "python3 -B tb/verilator/ctrl_wire_timing/run.py --self-test"
run diff-check "git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 HEAD"
git status --short > $L/tree-after.txt
echo done >> $G/extra/jobs.txt
