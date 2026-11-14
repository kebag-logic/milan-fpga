#!/bin/bash
# Lane 897 round 3's gates no workflow job runs (round 2's lane_gates2.sh, with the gates #902 adds at its round 9:
# tier_grid, rows_tiers, the flip check's four forms, em_dash, attribute_grep, the coverage self-test, twin plants):
# one log and one rc per gate, never piped, on a clean clone of a commit, in order, in one of the parts that run side
# by side, each on its own clone. usage: lane_gates3.sh COMMIT TAG PART
set -u
H=$1 TAG=$2 PART=$3
BASE=cec88385ad0a0ec0d61b91597640797766e45010 TIERS=5b264bf26416108add32d7fe5abca5252ffde2cb R2=3bebf03a1d25bcbde9c0ec48dfd711af7280131e
T=/data-2/milan/tmp/897-a776
S=$T/scripts
W=$T/r3/wt/lane-$TAG-$PART
G=$T/r3/gates-out/lane-$TAG
mkdir -p "$G" "$T/r3/wt"
[ -d "$W" ] || bash "$S/clone.sh" "$W" "$H" > "$G/clone-$PART.log" 2>&1
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
. "$S/env.sh"
export TMPDIR=$T/r3/tmp/lane-$TAG-$PART MAKEFLAGS="-j8 --no-print-directory" TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
mkdir -p "$TMPDIR"
run() { id=$1; shift; case " ${ONLY[*]} " in *" $id "*) ;; *) return;; esac
    { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"; echo "$(date +%T) $id rc=$rc" >> "$G/summary.txt"; }
case $PART in
  a) ONLY=(diffcheck_base diffcheck_tiers diffcheck_r2 em_dash_base em_dash_tiers tier_grid py_idiom cpp_idiom baremetal
           docs_check ctrl_hot_selftest ctrl_hot_check harness_selftest rows_tiers_selftest rows_tiers_report_exits_1
           load_selftest load_check flip_selftest flip_check_exits_1 flip_check_1x1 flip_check_1x1_as_built_exits_1
           flip_check_8x8_exits_1 attribute_grep hooks_selftest target_selftest gen_mailbox gen_mailbox_selftest lint_rtl
           soc_options ctrl_memory fw_coverage_selftest fw_coverage_check behave twin twin_plants);;
  b) ONLY=(test_builder);;
  c) ONLY=(plat_ledger fixtures boot_1x1 boot_8x8 boot_8x8_if2 boot_native boot_plants nvm_selftest);;
  rom) ONLY=(plat_ledger fixtures);;
  cov) ONLY=(fw_coverage_check);;
esac
B=$T/r3/builds/boot-$TAG
echo "$(date +%T) start $H part $PART" >> "$G/summary.txt"
run diffcheck_base "git diff --check $BASE HEAD"
run diffcheck_tiers "git diff --check $TIERS HEAD"
run diffcheck_r2 "git diff --check $R2 HEAD"
run em_dash_base "$T/gates/venv/bin/python3 -B scripts/check_em_dash.py --base $BASE"
run em_dash_tiers "$T/gates/venv/bin/python3 -B scripts/check_em_dash.py --base $TIERS"
run tier_grid "python3 -B tb/verilator/ctrl_service_budget/tier_grid.py --point 1x1/1if"
run py_idiom "python3 -B scripts/check_py_idiom.py"
run cpp_idiom "python3 -B scripts/check_cpp_idiom.py"
run baremetal "python3 scripts/check_baremetal_only.py --check"
run docs_check "python3 -B scripts/docs_check.py"
run ctrl_hot_selftest "python3 -B sw/firmware/ctrl/test/ctrl_hot.py --self-test"
run ctrl_hot_check "python3 -B sw/firmware/ctrl/test/ctrl_hot.py --check"
run harness_selftest "python3 -B tb/verilator/ctrl_service_budget/run.py --self-test"
run rows_tiers_selftest "python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --selftest"
# the tier model's report over both points exits 1 by design: 8x8/2if's rows are reported, not held (#894)
run rows_tiers_report_exits_1 "python3 -B tb/verilator/ctrl_service_budget/rows_tiers.py --terms"
run load_selftest "python3 -B tb/verilator/ctrl_service_budget/load_grade.py --selftest"
run load_check "python3 -B tb/verilator/ctrl_service_budget/load_grade.py --check"
run flip_selftest "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --selftest"
# the flip check over both points, as built at 1x1/1if, and at 8x8/2if exit 1 by design (#894's round 9); the 1x1/1if
# check with the built design is the flip's, held here (#894 ruling issuecomment-6867393730, item (d))
run flip_check_exits_1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check"
run flip_check_1x1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if"
run flip_check_1x1_as_built_exits_1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if --design as-built"
run flip_check_8x8_exits_1 "python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/2if"
run attribute_grep "git grep -n __attribute__ -- sw/firmware/ctrl ':!*/test/*'"
run hooks_selftest "python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test"
run target_selftest "python3 -B tb/verilator/nvm_split_target/run.py --self-test"
run gen_mailbox "python3 sw/mailbox/gen_mailbox.py --check --crosscheck"
run gen_mailbox_selftest "python3 sw/mailbox/gen_mailbox.py --selftest"
run lint_rtl "python3 scripts/lint_rtl.py --check"
run soc_options "python3 sw/builder/test_soc_options.py"
run ctrl_memory "python3 sw/litex/test_ctrl_memory.py"
run fw_coverage_selftest "python3 -B sw/firmware/gtest/fw_coverage.py --selftest"
run fw_coverage_check "python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 8"
run test_builder "python3 sw/builder/test_builder.py --require-rv32"
run plat_ledger "python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir $B/plat-ledger --self-test"
run fixtures "bash $S/r3/fixtures3.sh \$PWD $B/plat-ledger $B/fixtures && for f in $B/fixtures/*.rc; do [ \"\$(cat \$f)\" = 0 ] || exit 1; done"
run boot_1x1 "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $B/1x1"
run boot_8x8 "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $B/8x8 --shape endstation_ax7101_8x8"
run boot_8x8_if2 "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $B/8x8-if2 --shape endstation_ax7101_8x8 --interfaces 2"
run boot_native "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $B/native --native-controls"
run boot_plants "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $B/plants --self-test"
run nvm_selftest "python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8"
run behave "cd tests && $T/gates/venv/bin/behave --no-capture -f plain"
run twin "make -C tb/verilator/milan_dp twin"
run twin_plants "make -C tb/verilator/milan_dp twin-plants"
git status --short --untracked-files=all > "$G/tree-after-$PART.txt"
echo "$(date +%T) done part $PART" >> "$G/summary.txt"
