#!/usr/bin/env bash
# Documentation gates for a Markdown-only change, run at the checkout's HEAD.
# Each command's output and exit status are recorded; nothing is written to
# the checkout (python3 -B). Usage: docs_gates.sh <checkout> <base-rev> <round-base-rev>
set -u
repo=${1:?checkout}; base=${2:?base}; rbase=${3:?round base}
cd "$repo" || exit 2
echo "# head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}') at $(date -u +%FT%TZ)"
git submodule status
run() { echo "### $*"; "$@" 2>&1 | tail -n 6; echo "exit=${PIPESTATUS[0]}"; }
run python3 -B scripts/docs_check.py
run python3 -B scripts/check_em_dash.py --base "$base"
run python3 -B scripts/check_em_dash.py --base "$rbase"
run python3 -B scripts/check_em_dash.py --selftest
run python3 -B scripts/check_feature_status.py --self-test
run python3 -B scripts/check_baremetal_only.py --check
run python3 -B docs/traceability/gen_module_matrix.py --check
run python3 -B scripts/check_gptp_docs.py --with-submodule
run python3 -B scripts/check_gptp_docs.py --selftest
run python3 -B scripts/check_doc_style.py
run python3 -B scripts/check_doc_style.py --selftest
run python3 -B scripts/gen_toc.py --check
run python3 -B scripts/gen_toc.py --verify-anchors
run python3 -B scripts/check_doc_paths.py
run python3 -B scripts/check_submodule_docs.py
run python3 -B scripts/check_solution_docs.py
run python3 -B scripts/check_wire_accountability.py
run git diff --check "$base" HEAD
run git diff --check "$rbase" HEAD
echo "### worktree after gates"; git status --porcelain=v1 --ignored --untracked-files=all | head; echo "status-lines=$(git status --porcelain=v1 --ignored --untracked-files=all | wc -l)"
