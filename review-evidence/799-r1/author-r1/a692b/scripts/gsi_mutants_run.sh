#!/usr/bin/env bash
# #799: make gsi-mutants (milan_dp's #790 campaign: the clean obj_notify leg, then every planted arm) in a clean clone at <rev>.
# usage: gsi_mutants_run.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/799-a692b; C=$X/clone-gsi-${rev:0:8}; O=$X/r/gsi-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
cd "$C/tb/verilator/milan_dp" || exit 2
source "$D/env.sh"; export VERILATOR_JOBS=4
git -C "$C" rev-parse HEAD > "$O/head.txt"
s=$(date +%s); make gsi-mutants > "$O/make-gsi-mutants.log" 2>&1; rc=$?
echo "rc=$rc $(( $(date +%s)-s ))s" > "$O/rc.txt"
git -C "$C" status --porcelain --untracked-files=no > "$O/clone-status-after.txt"
echo GSI-DONE >> "$O/rc.txt"
