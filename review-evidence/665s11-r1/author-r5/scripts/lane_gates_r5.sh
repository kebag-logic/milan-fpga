#!/bin/bash
# lane_gates_r5.sh COMMIT GROUP: the lane's gates no workflow job runs (round 5, after #902's own list), one log and one
# rc per gate, never piped, in order, on a clean clone of COMMIT of the group's own, under r5/pass/lane-GROUP.
#   model  whitespace against three bases, the coverage gate's self-test, the tier, load, flip, pace and bound rules
#          and their self-tests, the idiom, documentation and statement gates, the mailbox generator, the RTL lint, the
#          SoC options, the memory ledger and the platform's ledgered images (the firmware campaigns, suites and
#          coverage ratchet are the rtl-fast firmware jobs')
#   sims1  the harness self-test, the hooks self-test, the saved-state target's self-test, behave, the datapath twin
#   sims2  the REBOOT simulation and its self-test, the split boot simulations
#   reboot the REBOOT simulation and its self-test alone
#   final  whitespace and the idiom and documentation gates alone
#   build  the end-station builder
#   nvm    the saved-state store's planted-defect campaign
set -u
H=$1 GROUP=$2
T=<scratch>
R=${PASS_ROOT:-$T/r5/pass}
W=$R/lane-$GROUP/wt
G=$R/lane
mkdir -p "$G" "$R/lane-$GROUP/scratch"
[ -d "$W" ] || bash "$T/r5/scripts/clone.sh" "$W" "$H" > "$G/clone-$GROUP.log" 2>&1
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
test -z "$(git status --porcelain --untracked-files=all)" || exit 5
git status --porcelain --untracked-files=all > "$G/$GROUP-tree-before.txt"
. "$T/tools/env.sh"
export PYTHONHASHSEED=0 TMPDIR=$R/lane-$GROUP/tmp MAKEFLAGS="-j8 --no-print-directory"
export TSN_GEN_ROOT=<management>/tools/tsn-gen-deca300c
mkdir -p "$TMPDIR"
S=$R/lane-$GROUP/scratch
V=$T/venv/bin/python3
run() { id=$1; shift
    { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"
    echo "$(date +%T) $id rc=$rc" >> "$G/summary-$GROUP.txt"; }
echo "$(date +%T) start $H group $GROUP" >> "$G/summary-$GROUP.txt"
B=tb/verilator/ctrl_service_budget
case $GROUP in
  model)
    run diffcheck_merge_base "git diff --check \$(git merge-base HEAD origin/dev-soft-core) HEAD"
    run diffcheck_round4 "git diff --check 049f0e4dd7b0b514d1ea9689822901750129c044 HEAD"
    run diffcheck_902 "git diff --check 41ca9f876b01e4af84d872b8bdbd751cc09debe0 HEAD"
    run fw_coverage_selftest "python3 -B sw/firmware/gtest/fw_coverage.py --selftest"
    run tier_grid "python3 -B $B/tier_grid.py --point 1x1/1if"
    run rows_tiers_selftest "python3 -B $B/rows_tiers.py --selftest"
    run rows_tiers_report_exits_1 "python3 -B $B/rows_tiers.py --terms"
    run load_selftest "python3 -B $B/load_grade.py --selftest"
    run load_check "python3 -B $B/load_grade.py --check"
    run flip_selftest "python3 -B $B/flip_grade.py --selftest"
    run flip_check_exits_1 "python3 -B $B/flip_grade.py --check"
    run flip_check_1x1 "python3 -B $B/flip_grade.py --check --point 1x1/1if"
    run flip_check_1x1_as_built_exits_1 "python3 -B $B/flip_grade.py --check --point 1x1/1if --design as-built"
    run flip_check_8x8_exits_1 "python3 -B $B/flip_grade.py --check --point 8x8/2if"
    run record_classes_selftest "python3 -I $B/record_classes.py --selftest"
    run rules "python3 -I -c \"import sys, pathlib; sys.path.insert(0, '$B'); import queued_bound, paced_rows, rows_tiers; r = pathlib.Path('.'); w = rows_tiers.solve('last', rows_tiers.point_inputs(r, '1x1/1if'), rows_tiers.BUILT)[0]; print('last', w, 'ruled', queued_bound.ruled(w), 'stated', queued_bound.stated(r)); s = queued_bound.statements(r) + paced_rows.statements(r) + rows_tiers.tx_statements(r); print('pace', paced_rows.choice(r), 'statements', s); print('controls escaped', queued_bound.controls(r) + paced_rows.controls(r)); sys.exit(1 if s else 0)\""
    run ctrl_hot_selftest "python3 -B sw/firmware/ctrl/test/ctrl_hot.py --self-test"
    run ctrl_hot_check "python3 -B sw/firmware/ctrl/test/ctrl_hot.py --check"
    run py_idiom "python3 -B scripts/check_py_idiom.py"
    run cpp_idiom "python3 -B scripts/check_cpp_idiom.py"
    run baremetal "python3 scripts/check_baremetal_only.py --check"
    run docs_check "python3 -B scripts/docs_check.py"
    run em_dash "$V -B scripts/check_em_dash.py --base \$(git merge-base HEAD origin/dev-soft-core)"
    run attribute_grep "git grep -n __attribute__ -- sw/firmware/ctrl ':!*/test/*'"
    run gen_mailbox "python3 sw/mailbox/gen_mailbox.py --check --crosscheck"
    run gen_mailbox_selftest "python3 sw/mailbox/gen_mailbox.py --selftest"
    run lint_rtl "python3 scripts/lint_rtl.py --check"
    run soc_options "python3 sw/builder/test_soc_options.py"
    run ctrl_memory "python3 sw/litex/test_ctrl_memory.py"
    run plat_ledger "python3 -B tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir $S/plat-ledger"
    ;;
  sims1)
    run harness_selftest "python3 -B $B/run.py --self-test"
    run hooks_selftest "python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test"
    run target_selftest "python3 -B tb/verilator/nvm_split_target/run.py --self-test"
    run behave "cd tests && $T/venv/bin/behave --no-capture -f plain"
    run twin "make -C tb/verilator/milan_dp twin"
    ;;
  sims2)
    run reboot_selftest "env -u PYTHONHASHSEED python3 -B tb/verilator/ctrl_reboot/run.py --build-dir $S/reboot-plants --self-test --jobs 3"
    run reboot_plain "env -u PYTHONHASHSEED python3 -B tb/verilator/ctrl_reboot/run.py --build-dir $S/reboot-plain"
    run boot_1x1 "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $S/boot-1x1"
    run boot_8x8 "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $S/boot-8x8 --shape endstation_ax7101_8x8"
    run boot_native "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $S/boot-native --native-controls"
    run boot_plants "python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir $S/boot-plants --self-test"
    ;;
  reboot)
    run reboot_selftest "env -u PYTHONHASHSEED python3 -B tb/verilator/ctrl_reboot/run.py --build-dir $S/reboot-plants --self-test --jobs 3"
    run reboot_plain "env -u PYTHONHASHSEED python3 -B tb/verilator/ctrl_reboot/run.py --build-dir $S/reboot-plain"
    ;;
  final)
    run diffcheck_merge_base "git diff --check \$(git merge-base HEAD origin/dev-soft-core) HEAD"
    run diffcheck_round4 "git diff --check 049f0e4dd7b0b514d1ea9689822901750129c044 HEAD"
    run diffcheck_902 "git diff --check 41ca9f876b01e4af84d872b8bdbd751cc09debe0 HEAD"
    run py_idiom "python3 -B scripts/check_py_idiom.py"
    run cpp_idiom "python3 -B scripts/check_cpp_idiom.py"
    run docs_check "python3 -B scripts/docs_check.py"
    ;;
  build)
    run test_builder "python3 sw/builder/test_builder.py --require-rv32"
    ;;
  nvm)
    run nvm_selftest "python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 8"
    ;;
  *)
    echo "unknown group $GROUP"; exit 2
    ;;
esac
git status --porcelain --untracked-files=all > "$G/$GROUP-tree-after.txt"
echo "$(date +%T) done group $GROUP" >> "$G/summary-$GROUP.txt"
