#!/bin/bash
# extra.sh: the assignment's named gates beyond the workflows, one log and rc each, on a fresh clone of the gate head
: "${CPUS:?CPUS unset}"
set -u
# claimed once: chain D reaches this after its Yosys shards, but the gates ran earlier in a unit of their own
mkdir <scratch>/gates/extra-claim 2>/dev/null || { echo "extra.sh already claimed, $(date -u +%FT%TZ)" >> <scratch>/gates/extra-claim.log; exit 0; }
G=<scratch>/gates; H=$(cat $G/HEAD); W=$G/extra/wt; L=$G/extra/logs; mkdir -p $L
[ -d $W ] || bash <scratch>/clone_at.sh $H $W > $L/clone.log 2>&1
cd $W || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
export HOME=$G/home VERILATOR=<data>/tools/pinned-verilator-5.050/verilator TMPDIR=$G/extra/tmp PYTHONHASHSEED=0 \
  COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true TSN_GEN_ROOT=<home>/milan-fpga-management/tools/tsn-gen-deca300c
mkdir -p $TMPDIR
BASE=<data>/tools/pinned-verilator-5.050:<data>/tools/sv2v-v0.0.12:<data>/scratch/a662/make43/bin:/usr/local/bin:/usr/bin:/bin
LITEX=<home>/litex-milan/venv/bin; MD=<data>/tools/md-venv-40cdefe08ebd/bin
run() { id=$1; p=$2; shift 2; { echo "# head $H gate $id: $*"; PATH=$p:$BASE taskset -c "$CPUS" bash -c "$*"; } > "$L/$id.log" 2>&1; rc=$?; echo $rc > "$L/$id.rc"; echo "$id rc=$rc" >> $G/extra/jobs.txt; }
run diff-check $MD "git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 HEAD"
run tally-mutants $MD "python3 sw/firmware/gtest/tally_selftest.py --mutants"
run nvm-self-test $MD "python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8"
run test-builder $LITEX "python3 sw/builder/test_builder.py --require-rv32"
run budget-self-test $LITEX "python3 -B tb/verilator/ctrl_service_budget/run.py --self-test"
run budget-1x1 $LITEX "python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir $G/extra/budget-1x1 --record-budget-findings"
run budget-8x8 $LITEX "python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir $G/extra/budget-8x8 --record-budget-findings"
run wire-8x8-none $LITEX "python3 -B tb/verilator/ctrl_wire_timing/run.py --point 8x8 --build-dir $G/extra/wire-8x8 --draws 16 --load none --out $G/extra/wire-8x8-none"
run wire-8x8-composed $LITEX "python3 -B tb/verilator/ctrl_wire_timing/run.py --reuse-build --build-dir $G/extra/wire-8x8 --draws 16 --load composed --out $G/extra/wire-8x8-composed"
git status --short > $L/tree-after.txt
echo done >> $G/extra/jobs.txt
