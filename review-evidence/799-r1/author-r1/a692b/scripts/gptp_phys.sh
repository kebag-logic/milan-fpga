#!/usr/bin/env bash
# #799: the scheduled physical gPTP suite (milan_dp_gptp, the shared milan_dp ax1x1gptp recipe) through the sweep
# driver, in a clean clone at <rev>, then the driver's tally.
# usage: gptp_phys.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/799-a692b; C=$X/clone-gptp-${rev:0:8}; O=$X/r/gptp-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
cd "$C" || exit 2
source "$D/env.sh"; export VERILATOR_JOBS=4 TSN_GEN_ROOT=$VALIDATION_STORAGE/scratch/a662/tsn-gen
git rev-parse HEAD > "$O/head.txt"
s=$(date +%s); bash scripts/run_all_suites.sh "$O/logs" --wait --physical-gptp > "$O/sweep.out" 2>&1; rc=$?
echo "$rc $(( $(date +%s)-s ))s run_all_suites --physical-gptp" > "$O/table.txt"
python3 scripts/suite_tally.py "$O/logs" > "$O/tally.out" 2>&1; echo "$? suite_tally" >> "$O/table.txt"
git status --porcelain --untracked-files=no > "$O/clone-status-after.txt"
echo GPTP-DONE >> "$O/table.txt"
