#!/usr/bin/env bash
# #818 (the #803 and #787 lanes' runner, paths only): the rtl-fast workflow replica (rtl_fast_steps.py) at <rev> in a clean clone
# whose origin/dev is the live remote dev tip, for the jobs named after <rev> (all needed jobs when none is named).
# RTLFAST_HOME holds the pinned RV32 SDK installed by scripts/ci_rv32_sdk.py --archive.
# usage: rtlfast_run.sh <rev> [job ...]
set -u
rev=$1; shift; X=$VALIDATION_STORAGE/scratch/818-a710b; C=$X/clone-rtlfast-${rev:0:8}; O=$X/r/rtlfast-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
source "$D/env.sh"; source "$D/fw_env.sh"
export RTLFAST_HOME=$VALIDATION_STORAGE/scratch/803-a693/sdk VERILATOR_JOBS=4
git -C "$C" rev-parse refs/remotes/origin/dev > "$O/base.txt"
s=$(date +%s)
$VALIDATION_STORAGE/scratch/a662/ci312/bin/python3 "$D/rtl_fast_steps.py" "$O/run" "$C" "$rev" "$@" > "$O/run.out" 2>&1; rc=$?
echo "$rc $(( $(date +%s)-s ))s rtl_fast_steps $*" > "$O/table.txt"
echo RTLFAST-DONE >> "$O/table.txt"
