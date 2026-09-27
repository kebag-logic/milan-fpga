#!/usr/bin/env bash
# R347-5 focused gate rerun. Usage: run_gates.sh <repo-root> <receipts-dir> <tmp-dir>
# Runs each gate in the foreground from the repo root; records rc per gate.
set -u
repo=$1; out=$2; tmp=$3
mkdir -p "$out" "$tmp"
export TMPDIR=$tmp PYTHONDONTWRITEBYTECODE=1
cd "$repo" || exit 2
base=ac18b50968b12efe4d15c0a06301264b35656b31
summary="$out/gate-summary.txt"
: > "$summary"
run() {
  local name=$1; shift
  "$@" > "$out/$name.log" 2>&1
  local rc=$?
  printf '%-28s rc=%s  %s\n' "$name" "$rc" "$*" | tee -a "$summary"
}
run planner-self-test      python3 -B tb/tools/torture_campaign.py --self-test
run release-mutants        python3 -B tb/tools/torture_release_mutants.py
run behave-plan            python3 -B -m behave tests/features/torture_campaign_plan.feature -f plain --no-capture
run behave-torture-tier    python3 -B -m behave tests/features --tags=@torture -f progress
run feature-status-selftest python3 -B scripts/check_feature_status.py --self-test
run feature-status         python3 -B scripts/check_feature_status.py
run docs-check             python3 -B scripts/docs_check.py
run doc-paths              python3 -B scripts/check_doc_paths.py
run doc-style              python3 -B scripts/check_doc_style.py
run py-idiom               python3 -B scripts/check_py_idiom.py
run em-dash                python3 -B scripts/check_em_dash.py --base $base
run gen-toc                python3 -B scripts/gen_toc.py --check
run coverage-by-area       python3 -B tb/tools/torture_campaign.py --coverage-by-area --areas soak,power
run plan-json              python3 -B tb/tools/torture_campaign.py --plan --areas soak,power --json
run diff-check-delta       git diff --check 54d9beea2888bd07369e67e5cb025d1405d03495 07f72ad640f99c43bc1354642ad4d7ed8ba410cc
run diff-check-base        git diff --check $base 07f72ad640f99c43bc1354642ad4d7ed8ba410cc
run worktree-clean         git status --porcelain=v1 --untracked-files=all
