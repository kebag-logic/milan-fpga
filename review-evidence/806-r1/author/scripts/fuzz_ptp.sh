#!/usr/bin/env bash
# fuzz_ptp.sh <rev>: make -C tb/verilator/tsn_fuzz ptp in a clean clone at <rev> (tsn-gen at the CI pin), then the
# campaign artifact's diff against the tree.
set -u
rev=$1; X=$VALIDATION_STORAGE/scratch/806-a701; C=$X/clone-fuzz-${rev:0:8}; O=$X/r/fuzz-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$O"
[ -d "$C" ] || bash "$D/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1 || exit 2
cd "$C" || exit 2
source "$D/env.sh"
git rev-parse HEAD > "$O/head.txt"; git -C "$TSN_GEN_ROOT" rev-parse HEAD > "$O/tsn-gen.txt"
s=$(date +%s); make -C tb/verilator/tsn_fuzz ptp > "$O/ptp.log" 2>&1; rc=$?
echo "$rc $(( $(date +%s)-s ))s make -C tb/verilator/tsn_fuzz ptp" > "$O/table.txt"
git diff --stat > "$O/tree-after.txt"; git diff > "$O/tree-after.diff"
echo FUZZ-DONE >> "$O/table.txt"
