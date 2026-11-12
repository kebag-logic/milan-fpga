#!/bin/bash
# The lane's gates no workflow job runs, one log and one rc per gate, never piped, on a clean clone of a commit, in
# order, in one of three parts that run side by side, each on its own clone. usage: lane_gates.sh COMMIT TAG PART
set -u
H=$1 TAG=$2 PART=$3
S=<scratch>/scripts
T=<scratch>
W=$T/lane-wt-$TAG-$PART
G=$T/gates-out/lane-$TAG
mkdir -p "$G"
[ -d "$W" ] || bash "$S/clone.sh" "$W" "$H" > "$G/clone.log" 2>&1
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
. "$S/env.sh"
export TMPDIR=$T/tmp-lane-$TAG-$PART MAKEFLAGS="-j8 --no-print-directory" TSN_GEN_ROOT=<management>/tools/tsn-gen-deca300c
mkdir -p "$TMPDIR"
run() { id=$1; shift; case " ${ONLY[*]} " in *" $id "*) ;; *) return;; esac
    { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$(date +%T) $id rc=$rc" >> "$G/summary.txt"; }
case $PART in
  a) ONLY=(diffcheck_merge_base diffcheck_round py_idiom cpp_idiom baremetal docs_check ctrl_hot_selftest ctrl_hot_check
           harness_selftest load_selftest load_check flip_selftest flip_check_exits_1 flip_check_1x1_exits_1
           flip_check_8x8_exits_1 probe_r711_1x1_column probe_r712_pin_1x1 attribute_grep hooks_selftest target_selftest
           gen_mailbox gen_mailbox_selftest lint_rtl soc_options ctrl_memory behave twin);;
  b) ONLY=(test_builder);;
  c) ONLY=(nvm_selftest boot_1x1 boot_8x8 boot_native boot_plants);;
esac
B=$T/boot-$TAG
echo "$(date +%T) start $H part $PART" >> "$G/summary.txt"
run diffcheck_merge_base "git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 HEAD"
run diffcheck_round "git diff --check e7e2b7444a9859b058deff0d9edb575f2fb1946f HEAD"
run py_idiom "python3 -B scripts/check_py_idiom.py"
run cpp_idiom "python3 -B scripts/check_cpp_idiom.py"
run baremetal "python3 scripts/check_baremetal_only.py --check"
run docs_check "python3 -B scripts/docs_check.py"
run ctrl_hot_selftest "python3 -B sw/firmware/ctrl/test/ctrl_hot.py --self-test"
run ctrl_hot_check "python3 -B sw/firmware/ctrl/test/ctrl_hot.py --check"
run harness_selftest "python3 -B tb/verilator/ctrl_service_budget/run.py --self-test"
run load_selftest "python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest"
run load_check "python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check"
run flip_selftest "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest"
# the flip check is no merge gate: it holds 8x8/2if at the pin and both points' rows by every source, and exits 1 at
# this head (the round 28 ruling, item 4: a 1x1/1if row's miss is a finding, not a STOP)
run flip_check_exits_1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check"
run flip_check_1x1_exits_1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if"
run flip_check_8x8_exits_1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/2if"
run probe_r711_1x1_column "python3 -I <management>/2026-09-23/665s2b-r711-6/scripts/probe_1x1_column.py \$PWD"
run probe_r712_pin_1x1 "python3 -I <management>/2026-09-23/665s2b-r712-6/scripts/probe_pin_1x1.py \$PWD"
run attribute_grep "git grep -n __attribute__ -- sw/firmware/ctrl ':!*/test/*'"
run hooks_selftest "python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test"
run target_selftest "python3 -B tb/verilator/nvm_split_target/run.py --self-test"
run nvm_selftest "python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8"
run gen_mailbox "python3 sw/mailbox/gen_mailbox.py --check --crosscheck"
run gen_mailbox_selftest "python3 sw/mailbox/gen_mailbox.py --selftest"
run lint_rtl "python3 scripts/lint_rtl.py --check"
run soc_options "python3 sw/builder/test_soc_options.py"
run ctrl_memory "python3 sw/litex/test_ctrl_memory.py"
run test_builder "python3 sw/builder/test_builder.py --require-rv32"
run boot_1x1 "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $B/1x1"
run boot_8x8 "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $B/8x8 --shape endstation_ax7101_8x8"
run boot_native "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $B/native --native-controls"
run boot_plants "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $B/plants --self-test"
run behave "cd tests && <scratch>/gates/venv/bin/behave --no-capture -f plain"
run twin "make -C tb/verilator/milan_dp twin"
git status --short --untracked-files=all > "$G/tree-after-$PART.txt"
echo "$(date +%T) done part $PART" >> "$G/summary.txt"
