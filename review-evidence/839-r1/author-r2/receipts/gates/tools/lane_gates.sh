#!/usr/bin/env bash
# lane_gates.sh <head sha> <group>: round 2's lane gates, one log and one rc per gate, never piped, on one clean
# clone of the head. Groups: light (beside the sweep), heavy (after it). Each log's first line names the head.
set -u
H=$1; GROUP=$2
S=$VALIDATION_STORAGE/839-a731b; W=$S/gates/lane-wt-${H:0:8}; G=$S/gates/lane-logs-${H:0:8}
T=$MANAGEMENT/2026-09-23/839-a731b/receipts/gates/tools
mkdir -p "$G" "$S/gates/tmp"
[ -d "$W" ] || "$T/clone_at.sh" "$H" "$W" || exit 3
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
BASE=$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
DOCS=$VALIDATION_STORAGE/sync-a723b/venv-docs/bin
export HOME=$WORKSPACE_HOME VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator TMPDIR=$S/gates/tmp \
  TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c MAKEFLAGS="-j16 --no-print-directory" \
  CI_CAMPAIGN_JOBS=8 PYTHONHASHSEED=0
run() { id=$1; shift; { echo "# head $H gate $id: $*"; PATH=$P bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?
        echo $rc > "$G/$id.rc"; echo "$id rc=$rc"; }
case $GROUP in
light)
  P=$BASE
  run diffcheck "git diff --check 604899c08ff1cd1830e1dd08b733109ef852400c HEAD"
  # not a pass: rc 0 here only confirms the script is absent at the head and the base, so the gate cannot run
  run docs_inventory_absent "test -z \"\$(git ls-tree --name-only HEAD scripts/docs_inventory.py)\" && test -z \"\$(git ls-tree --name-only 604899c08ff1cd1830e1dd08b733109ef852400c scripts/docs_inventory.py)\" && echo 'scripts/docs_inventory.py is in neither tree: NOT RUN'"
  P=$DOCS:$BASE
  run behave "cd tests && behave"
  ;;
heavy)
  P=$BASE
  run fw_tally_selftest "python3 sw/firmware/gtest/tally_selftest.py"
  run fw_rv32_selftest "python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32"
  for k in 0 1 2 3; do
    run fw_selftest_$k "python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard $k/4"
  done
  run fw_nvm "python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4"
  run fw_coverage_selftest "python3 sw/firmware/gtest/fw_coverage.py --selftest"
  run fw_coverage_check "python3 sw/firmware/gtest/fw_coverage.py --check --jobs 8"
  run builder "python3 sw/builder/test_builder.py --require-rv32"
  run bootsa_mutants "make -C tb/verilator/milan_dp bootsa-mutants"
  ;;
*) echo "group light|heavy"; exit 2 ;;
esac
git status --porcelain > "$G/tree-after-$GROUP.txt"
echo done > "$G/DONE-$GROUP"
