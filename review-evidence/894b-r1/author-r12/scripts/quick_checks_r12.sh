#!/bin/bash
# Round 12's quick checks on a clean clone of a head (round 9's STOP ends the round before the final gates, as rounds 5 and 8 did):
# each harness tool the round changes or reads, its self-test and its check; the documents and idiom gates; the
# comment rule over the round's delta and the PR's; R844-1's audit; diff checks. One line a check: its rc and last line.
# usage: quick_checks_r8.sh CLONE HEAD
set -u
C=$1 H=$2 S=$(dirname "$(readlink -f "$0")")
cd "$C" || exit 3
test "$(git rev-parse HEAD)" = "$H" || exit 4
. /data-2/milan/tmp/894b-a781/scripts/env.sh
export TSN_GEN_ROOT=$MANAGEMENT/tools/tsn-gen-deca300c
echo "# quick checks at $H"
run() { out=$(bash -c "$2" 2>&1); rc=$?; echo "$1 rc=$rc: $(printf '%s\n' "$out" | grep -v '^$' | tail -1)"; }
B=tb/verilator/ctrl_service_budget
run shape_costs "python3 -I $B/shape_costs.py --check --selftest"
run flip_selftest "python3 -B $B/flip_grade.py --selftest"
run flip_check_1x1 "python3 -B $B/flip_grade.py --check --point 1x1/1if"
run flip_check_8x8_1if "python3 -B $B/flip_grade.py --check --point 8x8/1if"
run rows_tiers_selftest "python3 -B $B/rows_tiers.py --selftest"
run load_check "python3 -B $B/load_grade.py --check"
run load_selftest "python3 -B $B/load_grade.py --selftest"
run record_classes_selftest "python3 -I $B/record_classes.py --selftest"
run egress_ledger_selftest "python3 -I $B/egress_ledger.py --selftest"
run mixed_probe "bash $S/mixed_probe_gate.sh $B"
run docs_check "python3 -B scripts/docs_check.py"
run py_idiom "python3 -B scripts/check_py_idiom.py"
run cpp_idiom "python3 -B scripts/check_cpp_idiom.py"
run comment_scan_pr "python3 -I $S/comment_scan.py . 7398ec0aeea468d92ff642a03a06e291a0cd58d1 HEAD | grep -v '^\$'"
run comment_scan_round9 "python3 -I $S/comment_scan.py . acfa560112f8cf5f8adb2d979024fe29e01662fc HEAD | grep -v '^\$'"
run comment_scan_round10 "python3 -I $S/comment_scan.py . cd7d92ad5cd83abdf0e2e81809699192edb4cc05 HEAD | grep -v '^\$'"
run comment_scan_round11 "python3 -I $S/comment_scan.py . db6bc954dcf2076c415199e6600c2f78153e282d HEAD | grep -v '^\$'"
run comment_scan_round12 "python3 -I $S/comment_scan.py . 05a7ea82fa0625e077959cd1b4eed28a7a05b064 HEAD | grep -v '^\$'"
run diffcheck_round11_head "git diff --check 05a7ea82fa0625e077959cd1b4eed28a7a05b064 HEAD"
run r844_audit "bash $S/r844_audit_empty.sh /data-2/milan/tmp/894b-a781/r4/evidence/source_comment_audit.py"
run diffcheck_round8_head "git diff --check acfa560112f8cf5f8adb2d979024fe29e01662fc HEAD"
run diffcheck_round9_head "git diff --check cd7d92ad5cd83abdf0e2e81809699192edb4cc05 HEAD"
run diffcheck_70f4056f "git diff --check 70f4056f384e12520ccae254fe26f6286fd39db6 HEAD"
echo "# the clone after: $(git status --porcelain --untracked-files=all | wc -l) changed path(s)"
