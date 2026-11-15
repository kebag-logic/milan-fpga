#!/bin/bash
# gates.sh CLEAN AT41 PACKET EVDIR: this round's reruns on the clean clone CLEAN (exact head) and on AT41 (41ca9f87),
# concurrently, one log and rc each under PACKET/receipts/gates.
set -u
C=$1 A=$2 P=$3 E=$4 O=$3/receipts/gates B=tb/verilator/ctrl_service_budget
mkdir -p $O
export PYTHONHASHSEED=0
run() { id=$1 dir=$2; shift 2; ( cd "$dir" && { echo "# $(git rev-parse HEAD) $id: $*"; bash -c "$*"; } > $O/$id.log 2>&1; echo $? > $O/$id.rc ) & }
run flip_check_1x1 $C "python3 -I $B/flip_grade.py --check --point 1x1/1if"
run load_check $C "python3 -I $B/load_grade.py --check"
run load_selftest $C "python3 -I $B/load_grade.py --selftest"
run flip_selftest $C "python3 -I $B/flip_grade.py --selftest"
run polls_checks $C "cd $B && python3 -I -c \"import sys; sys.path.insert(0, '.'); import selftest, selftest_polls; c = selftest_polls.polls_checks(selftest.synthetic, selftest.SYS_HZ, selftest.CPU_HZ, selftest.tx_record); bad = [x for x in c if not x[1]]; print(f'polls checks: {len(c) - len(bad)} of {len(c)} pass'); [print('FAIL', x[0], x[2]) for x in bad]; sys.exit(1 if bad else 0)\""
run survey_head $C "python3 -I $E/author-r6/scripts/statement_survey.py ."
run survey_41ca9f87 $A "python3 -I $E/author-r6/scripts/statement_survey.py ."
run figures_head $C "python3 -I $P/scripts/figures_probe.py ."
run figures_41ca9f87 $A "python3 -I $P/scripts/figures_probe.py ."
run py_idiom $C "python3 -I scripts/check_py_idiom.py"
run cpp_idiom $C "python3 -I scripts/check_cpp_idiom.py"
run docs_check $C "python3 -I scripts/docs_check.py"
run doc_paths $C "python3 -I scripts/check_doc_paths.py"
run doc_style $C "python3 -I scripts/check_doc_style.py"
run diffcheck_round5 $C "git diff --check d3566d44dcae75069f56d97402a5f1b351743008 HEAD"
run delta_noncomment $C "git diff -U0 d3566d44dcae75069f56d97402a5f1b351743008 HEAD -- '*.c' '*.h' '*.cpp' '*.py' | grep -E '^[-+][^-+]' | grep -vE '^[-+][[:space:]]*(//|#)'"
wait
for f in $O/*.rc; do echo "$(basename $f .rc) rc=$(cat $f)"; done > $O/summary.txt
