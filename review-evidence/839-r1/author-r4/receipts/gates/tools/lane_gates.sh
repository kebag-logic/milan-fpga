#!/usr/bin/env bash
# lane_gates.sh <head sha>: round 4's lane gates (one merge base, git diff --check against it, docs_inventory.py
# --check and --selftest, bootsa, bootsa-mutants), one log and one rc per gate, never piped, on one clean clone of
# the head. Each log's first line names the head.
set -u
H=$1
L=$LANES/839-boot-sa
S=$VALIDATION_STORAGE/839-a731d; W=$S/gates/lane-wt-${H:0:8}; G=$S/gates/lane-logs-${H:0:8}
T=$MANAGEMENT/2026-09-23/839-a731d/receipts/gates/tools
mkdir -p "$G" "$S/gates/tmp"
[ -d "$W" ] || "$T/clone_at.sh" "$H" "$W" || exit 3
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
# origin/dev as the lane fetched it, so the merge base is computed in the clean clone
DEV=$(git -C "$L" rev-parse origin/dev)
git fetch -q "$L" "$DEV" || exit 5
P=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export HOME=$WORKSPACE_HOME VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$S/gates/tmp \
  TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c MAKEFLAGS="-j16 --no-print-directory" \
  CI_CAMPAIGN_JOBS=8 PYTHONHASHSEED=0
run() { id=$1; shift; { echo "# head $H gate $id: $*"; PATH=$P bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?
        echo $rc > "$G/$id.rc"; echo "$id rc=$rc"; }
run merge_base_one "echo origin/dev $DEV; git merge-base --all $DEV HEAD; test \$(git merge-base --all $DEV HEAD | wc -l) -eq 1 && test \$(git merge-base $DEV HEAD) = $DEV"
MB=$(git merge-base "$DEV" HEAD)
run diffcheck "git diff --check $MB HEAD"
run docs_inventory_check "python3 scripts/docs_inventory.py --check"
run docs_inventory_selftest "python3 scripts/docs_inventory.py --selftest"
run bootsa "make -C tb/verilator/milan_dp bootsa"
run bootsa_mutants "make -C tb/verilator/milan_dp bootsa-mutants"
git status --porcelain > "$G/tree-after.txt"
echo done > "$G/DONE"
