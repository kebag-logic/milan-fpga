#!/bin/bash
# A cost control's build and group run on a clean clone of a commit (run.py --mutation picks the plant's group); its
# logs are regraded at the final head with --reuse-build, which refuses unless every recorded input is unchanged.
# usage: ctl.sh COMMIT MUTATION [run.py args]
set -u
H=$1 M=$2; shift 2
T=<scratch>
. $T/scripts/env.sh
C=$T/L-CTL B=$T/builds/ctl-$M L=$T/logs/ctl-$M.log
export TMPDIR=$T/tmp-ctl-$M MAKEFLAGS="-j8 --no-print-directory"; mkdir -p "$TMPDIR"
test -d "$C" || exit 3
test "$(git -C "$C" rev-parse HEAD)" = "$H" || { echo "rc=4 clone not at $H" > "$L"; exit 4; }
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) control $M $*" > "$L"
start=$(date +%s)
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point 8x8 --build-dir "$B" --mutation "$M" \
    --record-budget-findings --record-share-findings --jobs 8 "$@" >> "$L" 2>&1
rc=$?
echo "elapsed=$(( $(date +%s) - start ))s rc=$rc" >> "$L"
git -C "$C" status --short --untracked-files=all > $T/logs/ctl-$M-tree-after.txt
echo $rc > "$L.rc"
