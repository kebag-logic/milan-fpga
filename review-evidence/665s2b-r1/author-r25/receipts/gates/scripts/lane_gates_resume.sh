#!/bin/bash
# The lane's gates no workflow job runs, one log and one rc per gate, never piped, on a clean clone of a commit, in
# order. usage: lane_gates.sh COMMIT TAG
set -u
H=$1 TAG=$2
S=<scratch>/scripts
T=<scratch>
W=$T/lane-wt-$TAG
G=$T/gates-out/lane-$TAG
mkdir -p "$G"
[ -d "$W" ] || bash "$S/clone.sh" "$W" "$H" > "$G/clone.log" 2>&1
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
. "$S/env.sh"
export TMPDIR=$T/tmp-lane-$TAG MAKEFLAGS="-j8 --no-print-directory" TSN_GEN_ROOT=<management>/tools/tsn-gen-deca300c
mkdir -p "$TMPDIR"
run() { id=$1; shift; if [ "$(cat "$G/$id.rc" 2>/dev/null)" = 0 ] && head -1 "$G/$id.log" | grep -q "head $H "; then echo "$(date +%T) $id rc=0 (kept: passed at this head before the 17:00 reset)" >> "$G/summary.txt"; return; fi; { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$(date +%T) $id rc=$rc" >> "$G/summary.txt"; }
B=$T/boot-$TAG
echo "$(date +%T) resume $H after the 17:00 host reset" >> "$G/summary.txt"
run diffcheck_merge_base "git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 HEAD"
run diffcheck_round "git diff --check a30c998627f356a63eaca10240f22fe70226261e HEAD"
run py_idiom "python3 -B scripts/check_py_idiom.py"
run cpp_idiom "python3 -B scripts/check_cpp_idiom.py"
run baremetal "python3 scripts/check_baremetal_only.py --check"
run docs_check "python3 -B scripts/docs_check.py"
run ctrl_hot_selftest "python3 -B sw/firmware/ctrl/test/ctrl_hot.py --self-test"
run ctrl_hot_check "python3 -B sw/firmware/ctrl/test/ctrl_hot.py --check"
run harness_selftest "python3 -B tb/verilator/ctrl_service_budget/run.py --self-test"
run load_selftest "python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest"
run load_check "python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check"
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
git status --short --untracked-files=all > "$G/tree-after.txt"
echo "$(date +%T) done" >> "$G/summary.txt"
