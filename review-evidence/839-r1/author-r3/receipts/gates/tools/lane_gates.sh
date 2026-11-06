#!/usr/bin/env bash
# lane_gates.sh <head sha>: round 3's lane gates (git diff --check, the docs_inventory presence probe, bootsa,
# bootsa-mutants), one log and one rc per gate, never piped, on one clean clone of the head. Each log's first
# line names the head.
set -u
H=$1
S=$VALIDATION_STORAGE/839-a731c; W=$S/gates/lane-wt-${H:0:8}; G=$S/gates/lane-logs-${H:0:8}
T=$MANAGEMENT/2026-09-23/839-a731c/receipts/gates/tools
mkdir -p "$G" "$S/gates/tmp"
[ -d "$W" ] || "$T/clone_at.sh" "$H" "$W" || exit 3
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
P=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export HOME=$WORKSPACE_HOME VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$S/gates/tmp \
  TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c MAKEFLAGS="-j16 --no-print-directory" \
  CI_CAMPAIGN_JOBS=8 PYTHONHASHSEED=0
run() { id=$1; shift; { echo "# head $H gate $id: $*"; PATH=$P bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?
        echo $rc > "$G/$id.rc"; echo "$id rc=$rc"; }
run diffcheck "git diff --check 604899c08ff1cd1830e1dd08b733109ef852400c HEAD"
# not a pass: rc 0 here only confirms the script is absent at the head and the base, so the gate cannot run
run docs_inventory_absent "test -z \"\$(git ls-tree --name-only HEAD scripts/docs_inventory.py)\" && test -z \"\$(git ls-tree --name-only 604899c08ff1cd1830e1dd08b733109ef852400c scripts/docs_inventory.py)\" && echo 'scripts/docs_inventory.py is in neither tree: NOT RUN'"
run bootsa "make -C tb/verilator/milan_dp bootsa"
run bootsa_mutants "make -C tb/verilator/milan_dp bootsa-mutants"
git status --porcelain > "$G/tree-after.txt"
echo done > "$G/DONE"
