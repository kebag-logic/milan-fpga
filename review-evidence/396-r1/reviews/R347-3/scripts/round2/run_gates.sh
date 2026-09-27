#!/usr/bin/env bash
# R347-2 gate runner. Usage: run_gates.sh <clone> <packet> <md-venv-python>
# Runs each gate in the foreground in <clone>, one log per gate under
# <packet>/receipts/, and a summary line per gate in gate-summary.txt.
set -u
clone=$1 packet=$2 mdpy=$3
base=ac18b50968b12efe4d15c0a06301264b35656b31
out=$packet/receipts
summary=$out/gate-summary.txt
: > "$summary"
cd "$clone" || exit 2
gate() {
  local name=$1; shift
  "$@" > "$out/$name.log" 2>&1
  local rc=$?
  echo "$name rc=$rc :: $*" | sed "s#$mdpy#\$MDPY#" >> "$summary"
}
gate planner-self-test python3 -B tb/tools/torture_campaign.py --self-test
gate behave-plan python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain
gate behave-torture-tier python3 -B -m behave tests/features --tags=@torture -f progress
gate feature-status-selftest python3 -B scripts/check_feature_status.py --self-test
gate feature-status python3 -B scripts/check_feature_status.py
gate docs-check python3 -B scripts/docs_check.py
gate doc-paths python3 -B scripts/check_doc_paths.py
gate doc-style python3 -B scripts/check_doc_style.py
gate py-idiom python3 -B scripts/check_py_idiom.py
gate em-dash "$mdpy" -B scripts/check_em_dash.py --base $base
gate gen-toc "$mdpy" -B scripts/gen_toc.py --check
gate diff-check-worktree git diff --check
gate diff-check-commit git diff $base HEAD --check
gate coverage-by-area python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power
gate plan-json python3 -B tb/tools/torture_campaign.py --plan --areas soak,power --json
cat "$summary"
