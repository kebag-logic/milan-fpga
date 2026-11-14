#!/bin/bash
# The lane's gates no workflow job runs, one log and one rc per gate, never piped, on a clean clone of a commit, in
# order, in one of three parts that run side by side, each on its own clone (round 2 phase B's lane_gates.sh; round 3 adds the diff checks against #902's head 7398ec0a and round 2's head 184d47ca).
# usage: lane_gates.sh COMMIT PART
set -u
H=$1 PART=$2
T=/data-2/milan/tmp/894b-a781
S=$T/scripts
W=$T/fullC/gate-wt-$PART
G=$T/fullC/lane
mkdir -p "$G"
[ -d "$W" ] || bash "$S/clone.sh" "$W" "$H" > "$G/clone-$PART.log" 2>&1
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
. "$S/env.sh"
export TMPDIR=$T/tmp/lane-$PART MAKEFLAGS="-j8 --no-print-directory" TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
mkdir -p "$TMPDIR"
run() { id=$1; shift; case " ${ONLY[*]} " in *" $id "*) ;; *) return;; esac
    { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$(date +%T) $id rc=$rc" >> "$G/summary.txt"; }
case $PART in
  a) ONLY=(diffcheck_merge_base diffcheck_round1 diffcheck_810 diffcheck_round3 diffcheck_round4 diffcheck_round5 diffcheck_810_084cf7a8 diffcheck_round6 diffcheck_round7_start diffcheck_lane_start diffcheck_902_round9_start diffcheck_902_head diffcheck_phase_a diffcheck_902_7398 diffcheck_round2_head em_dash tier_grid fw_coverage_selftest py_idiom cpp_idiom baremetal docs_check ctrl_hot_selftest
           ctrl_hot_check harness_selftest rows_tiers_selftest rows_tiers_report_exits_1 load_selftest load_check flip_selftest
           flip_check_exits_1 flip_check_1x1 flip_check_8x8_1if flip_check_1x1_as_built_exits_1 flip_check_8x8_exits_1 shape_costs
           probe_r711_1x1_column probe_r712_pin_1x1 attribute_grep hooks_selftest target_selftest gen_mailbox
           gen_mailbox_selftest lint_rtl soc_options ctrl_memory behave twin twin_plants);;
  b) ONLY=(test_builder);;
  c) ONLY=(nvm_selftest boot_1x1 boot_8x8 boot_native boot_plants);;
esac
B=$T/fullC/boot-gate
echo "$(date +%T) start $H part $PART" >> "$G/summary.txt"
run diffcheck_merge_base "git diff --check 1d6bf5556ae28764361d85012b86394eb467d294 HEAD"
run diffcheck_round1 "git diff --check f9442a10ff7e673c6e65874ca7629b49201c589d HEAD"
run diffcheck_810 "git diff --check 66f713267f201d1a00d7f711e04b3a996d804dee HEAD"
run diffcheck_round3 "git diff --check 64688da3b211e8e0e2b92b6c24e5ad3bd7490104 HEAD"
run diffcheck_round4 "git diff --check 66adb9a987b56c2b1a12ce92d058e0bc1a57bc3a HEAD"
run diffcheck_round5 "git diff --check 9d7167bd35afbf888ff0dcc1c10fe0e572ff6312 HEAD"
run diffcheck_810_084cf7a8 "git diff --check 084cf7a8455e9fa8e24a0e5bcf57c9557816c819 HEAD"
run diffcheck_round6 "git diff --check eebc37a32e15c81b3a855cdee49427e02c961590 HEAD"
run diffcheck_round7_start "git diff --check ccb47e39a534f4c8d02af826fa50fcd6578a38de HEAD"
run diffcheck_lane_start "git diff --check 8a3791e44533d6b1cc26d486d0b18e7d83470dc1 HEAD"
run diffcheck_902_round9_start "git diff --check dd01b0afef87037ec485cd49b40a26b542854bdd HEAD"
run diffcheck_902_head "git diff --check 5b264bf26416108add32d7fe5abca5252ffde2cb HEAD"
run diffcheck_phase_a "git diff --check bc8acc76fc524c167aa47613e54968e66ff02a17 HEAD"
run diffcheck_902_7398 "git diff --check 7398ec0aeea468d92ff642a03a06e291a0cd58d1 HEAD"
run diffcheck_round2_head "git diff --check 184d47cacc0b4eccb923cfbd4f2df9c3a05f5638 HEAD"
run em_dash "/data-2/milan/tmp/894-a773/venv-md/bin/python3 -B scripts/check_em_dash.py --base 66adb9a987b56c2b1a12ce92d058e0bc1a57bc3a"
# round 7 under #894's contingent ruling and its amendment: the grid holds the built design at 1x1/1if (exit 0)
run tier_grid "python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if"
run fw_coverage_selftest "python3 -B sw/firmware/gtest/fw_coverage.py --selftest"
run py_idiom "python3 -B scripts/check_py_idiom.py"
run cpp_idiom "python3 -B scripts/check_cpp_idiom.py"
run baremetal "python3 scripts/check_baremetal_only.py --check"
run docs_check "python3 -B scripts/docs_check.py"
run ctrl_hot_selftest "python3 -B sw/firmware/ctrl/test/ctrl_hot.py --self-test"
run ctrl_hot_check "python3 -B sw/firmware/ctrl/test/ctrl_hot.py --check"
run harness_selftest "python3 -B tb/verilator/ctrl_service_budget/run.py --self-test"
run rows_tiers_selftest "python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest"
run rows_tiers_report_exits_1 "python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --terms"
run load_selftest "python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest"
run load_check "python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check"
run flip_selftest "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest"
# the flip check is no merge gate: it holds 8x8/2if at the pin and both points' rows by every source; with the built
# design (#894) it exits 1 at 1x1/1if at #810's merged costs (round 6's STOP) and at 8x8/2if, an owner question; as
# built it exits 1 at 1x1/1if (R4)
run flip_check_exits_1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check"
# round 7 under #894's contingent ruling and its amendment: every 1x1/1if row holds by every source (exit 0)
run flip_check_1x1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if"
# the 8x8/1if follow-up (#894 issuecomment-6867393730, item (b)): its load at 0.75 and the table of shapes (exit 0)
run flip_check_8x8_1if "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if"
run shape_costs "python3 -I tb/verilator/ctrl_service_budget/shape_costs.py --check --selftest"
run flip_check_1x1_as_built_exits_1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if --design as-built"
run flip_check_8x8_exits_1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/2if"
run probe_r711_1x1_column "python3 -I $MANAGEMENT/2026-09-23/665s2b-r711-6/scripts/probe_1x1_column.py \$PWD"
run probe_r712_pin_1x1 "python3 -I $MANAGEMENT/2026-09-23/665s2b-r712-6/scripts/probe_pin_1x1.py \$PWD"
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
run behave "cd tests && /data-2/milan/tmp/894-a773/gates/venv/bin/behave --no-capture -f plain"
run twin "make -C tb/verilator/milan_dp twin"
run twin_plants "make -C tb/verilator/milan_dp twin-plants"
git status --short --untracked-files=all > "$G/tree-after-$PART.txt"
echo "$(date +%T) done part $PART" >> "$G/summary.txt"
