#!/bin/bash
# lane_gates_r6.sh COMMIT GROUP: round 6's gates on the clean clone r6/fc of COMMIT, one log and one rc per gate, never
# piped, in order (the gates the round's touched files feed: poll_grade.py, plat_mutants.py's and test_plat_boot.cpp's
# comments, ctrl_plat.h's comment, three Markdown files).
#   model    whitespace against three bases, the idiom and documentation gates, the model gates (R821-5's
#            model_gates.sh list, the tier grid and the rows' self-test), the statement survey, the polls checks
#   harness  the CPU budget harness's self-test, whose polls checks read poll_grade.STATED_US
set -u
H=$1 GROUP=$2
T=<scratch> R=$T/r6/pass W=$T/r6/fc G=$R/lane
mkdir -p "$G"
cd "$W" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
test -z "$(git status --porcelain --untracked-files=all)" || exit 5
git status --porcelain --untracked-files=all > "$G/$GROUP-tree-before.txt"
. "$T/tools/env.sh"
export PYTHONHASHSEED=0 TMPDIR=$R/tmp-$GROUP MAKEFLAGS="-j8 --no-print-directory"
mkdir -p "$TMPDIR"
V=$T/venv/bin/python3
B=tb/verilator/ctrl_service_budget
run() { id=$1; shift
    { echo "# head $H gate $id: $*"; bash -c "$*"; } > "$G/$id.log" 2>&1; rc=$?; echo $rc > "$G/$id.rc"
    echo "$(date +%T) $id rc=$rc" >> "$G/summary-$GROUP.txt"; }
echo "$(date +%T) start $H group $GROUP" >> "$G/summary-$GROUP.txt"
case $GROUP in
  model)
    run diffcheck_merge_base "git diff --check \$(git merge-base HEAD origin/dev-soft-core) HEAD"
    run diffcheck_round5 "git diff --check d3566d44dcae75069f56d97402a5f1b351743008 HEAD"
    run diffcheck_902 "git diff --check 41ca9f876b01e4af84d872b8bdbd751cc09debe0 HEAD"
    run py_idiom "python3 -B scripts/check_py_idiom.py"
    run cpp_idiom "python3 -B scripts/check_cpp_idiom.py"
    run docs_check "python3 -B scripts/docs_check.py"
    run doc_paths "python3 -B scripts/check_doc_paths.py"
    run doc_style "python3 -B scripts/check_doc_style.py"
    run em_dash "$V -B scripts/check_em_dash.py --base \$(git merge-base HEAD origin/dev-soft-core)"
    run toc_check "$V -B scripts/gen_toc.py --check"
    run toc_anchors "$V -B scripts/gen_toc.py --verify-anchors"
    run flip_check_1x1 "python3 -I $B/flip_grade.py --check --point 1x1/1if"
    run load_check "python3 -I $B/load_grade.py --check"
    run load_selftest "python3 -I $B/load_grade.py --selftest"
    run record_classes_selftest "python3 -I $B/record_classes.py --selftest"
    run flip_selftest "python3 -I $B/flip_grade.py --selftest"
    run rows_tiers_selftest "python3 -B $B/rows_tiers.py --selftest"
    run tier_grid "python3 -B $B/tier_grid.py --point 1x1/1if"
    run rules "python3 -I -c \"import sys, pathlib; sys.path.insert(0, '$B'); import queued_bound, paced_rows, rows_tiers; r = pathlib.Path('.'); w = rows_tiers.solve('last', rows_tiers.point_inputs(r, '1x1/1if'), rows_tiers.BUILT)[0]; print('last', w, 'ruled', queued_bound.ruled(w), 'stated', queued_bound.stated(r)); s = queued_bound.statements(r) + paced_rows.statements(r) + rows_tiers.tx_statements(r); print('pace', paced_rows.choice(r), 'statements', s); print('controls escaped', queued_bound.controls(r) + paced_rows.controls(r)); sys.exit(1 if s else 0)\""
    run statement_survey "python3 -I $T/r6/scripts/statement_survey.py ."
    run polls_checks "cd $B && python3 -I -c \"import sys; sys.path.insert(0, '.'); import selftest, selftest_polls; c = selftest_polls.polls_checks(selftest.synthetic, selftest.SYS_HZ, selftest.CPU_HZ, selftest.tx_record); bad = [x for x in c if not x[1]]; print(f'polls checks: {len(c) - len(bad)} of {len(c)} pass'); [print('FAIL', x[0], x[2]) for x in bad]; sys.exit(1 if bad else 0)\""
    run retained_equal "python3 -I -c \"import sys; sys.path.insert(0, '$B'); import poll_grade, load_grade; a = (poll_grade.STATED_US[1]['retained'], load_grade.STATED_US['1x1/1if']['item.retained'], load_grade.STATED_US_DONOR['1x1/1if']['item.retained'], load_grade.STATED_US['1x1/1if']['record.srp']); print('1x1/1if retained: poll_grade', a[0], 'load_grade pin', a[1], 'donor', a[2], 'record.srp', a[3]); sys.exit(0 if len(set(a)) == 1 else 1)\""
    ;;
  harness)
    run harness_selftest "python3 -B $B/run.py --self-test"
    ;;
  *) echo "unknown group $GROUP"; exit 2;;
esac
git status --porcelain --untracked-files=all > "$G/$GROUP-tree-after.txt"
echo "$(date +%T) done group $GROUP" >> "$G/summary-$GROUP.txt"
