#!/bin/bash
# A cost control's build and group run on a clean clone of a commit (run.py --mutation picks the plant's group).
# usage: ctl.sh CLONE COMMIT MUTATION [run.py args]
set -u
C=$1 H=$2 M=$3; shift 3
T=/data-2/milan/tmp/665s2b-a683zo
. $T/scripts/env.sh
B=$T/builds/ctl-$M-${H:0:8} L=$T/logs/ctl-$M-${H:0:8}.log
export TMPDIR=$T/tmp/ctl-$M MAKEFLAGS="-j12 --no-print-directory" PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR"
test -d "$C" || exit 3
test "$(git -C "$C" rev-parse HEAD)" = "$H" || { echo "rc=4 clone not at $H" > "$L"; exit 4; }
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) control $M $*" > "$L"
start=$(date +%s)
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point 8x8 --build-dir "$B" --mutation "$M" \
    --record-budget-findings --record-share-findings --jobs 2 "$@" >> "$L" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s rc=$rc" >> "$L"
git -C "$C" status --short --untracked-files=all > $T/logs/ctl-$M-${H:0:8}-tree-after.txt
echo $rc > "$L.rc"
