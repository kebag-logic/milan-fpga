#!/bin/bash
# The lane's standalone gates, one log and one rc per gate, never piped, on a clean clone of a commit, in order.
# usage: lane_gates.sh COMMIT TAG
set -u
H=$1 TAG=$2
S=$SCRATCH/scripts
T=$SCRATCH
W=$T/lane-wt-$TAG
G=$T/gates-out/lane-$TAG
mkdir -p "$G"
[ -d "$W" ] || bash "$S/clone.sh" "$W" "$H" > "$G/clone.log" 2>&1
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
. "$S/env.sh"
export TMPDIR=$T/tmp-lane-$TAG MAKEFLAGS="-j8 --no-print-directory" TSN_GEN_ROOT=$HOME/milan-fpga-management/tools/tsn-gen-deca300c
mkdir -p "$TMPDIR"
run() { id=$1; shift; { echo "# head $H gate $id: $*"; /usr/bin/time -f "# wall=%e s maxrss=%M kB" bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$(date +%T) $id rc=$rc" >> "$G/summary.txt"; }
echo "$(date +%T) start $H" >> "$G/summary.txt"
run diffcheck_merge_base "git diff --check a9d69c774d HEAD"
run docs_check "python3 -B scripts/docs_check.py"
run py_idiom "python3 -B scripts/check_py_idiom.py"
run baremetal "python3 scripts/check_baremetal_only.py --check"
run harness_selftest "python3 -B tb/verilator/ctrl_service_budget/run.py --self-test"
run hooks_selftest "python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test"
run target_selftest "python3 -B tb/verilator/nvm_split_target/run.py --self-test"
run nvm_selftest "python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8"
run gen_mailbox "python3 sw/mailbox/gen_mailbox.py --check --crosscheck"
run gen_mailbox_selftest "python3 sw/mailbox/gen_mailbox.py --selftest"
run ctrl_memory "python3 sw/litex/test_ctrl_memory.py"
run soc_options "python3 sw/builder/test_soc_options.py"
run test_builder "python3 sw/builder/test_builder.py --require-rv32"
run behave "cd tests && $SCRATCH/gates/venv/bin/behave --no-capture -f plain"
# a receipt, not a gate: the 32x32 point owes every save group to #823 and exits 1 building nothing
run receipt_target_32x32 "python3 -B tb/verilator/nvm_split_target/run.py --point 32x32 --build-dir $TMPDIR/nvm-target-32x32"
git status --short --untracked-files=all > "$G/tree-after.txt"
echo "$(date +%T) done" >> "$G/summary.txt"
