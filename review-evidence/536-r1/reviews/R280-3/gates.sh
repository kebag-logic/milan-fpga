#!/usr/bin/env bash
# Composition gates for PR #543 on the merge-train candidate.
# Usage: gates.sh <candidate-checkout> <parent-rev> <source-merge-base>
# Runs each gate in the foreground, prints one RESULT line per gate.
set -u
repo=${1:?candidate checkout}
parent=${2:?parent revision}
srcbase=${3:?source merge base}
cd "$repo" || exit 2
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
run() {
  local name=$1; shift
  echo "=== $name: $*"
  "$@"
  local rc=$?
  echo "RESULT $name rc=$rc"
}
run diff-check        git diff --check "$parent" HEAD
run docs_check        python3 -B scripts/docs_check.py
run em_dash_parent    python3 -B scripts/check_em_dash.py --base "$parent"
run em_dash_srcbase   python3 -B scripts/check_em_dash.py --base "$srcbase"
run em_dash_selftest  python3 -B scripts/check_em_dash.py --selftest
run doc_style         python3 -B scripts/check_doc_style.py
run doc_paths         python3 -B scripts/check_doc_paths.py
run toc_anchors       python3 -B scripts/gen_toc.py --verify-anchors
run toc_check         python3 -B scripts/gen_toc.py --check
run feature_status    python3 -B scripts/check_feature_status.py
run feature_status_st python3 -B scripts/check_feature_status.py --self-test
run solution_docs     python3 -B scripts/check_solution_docs.py
run submodule_docs    python3 -B scripts/check_submodule_docs.py
run gptp_docs         python3 -B scripts/check_gptp_docs.py
run gptp_docs_sub     python3 -B scripts/check_gptp_docs.py --with-submodule
run module_matrix     python3 -B docs/traceability/gen_module_matrix.py --check
run py_idiom          python3 -B scripts/check_py_idiom.py
run naming            python3 -B scripts/measure_naming.py --check
run fail_fast         python3 -B scripts/measure_fail_fast.py --check
run todo_ownership    python3 -B scripts/check_todo_ownership.py
run test_evidence     python3 -B scripts/measure_test_evidence.py --check
run hygiene           python3 -B scripts/check_hygiene.py --check
run port_contracts    python3 -B scripts/check_port_contracts.py
run pp_srcs_check     python3 -B scripts/pp_srcs.py --check
run ci_events_check   python3 -B scripts/ci_events.py --check
run behave_contract   bash -c 'cd tests && behave --no-capture -f plain features/aecp_response_contract.feature 2>&1 | tail -8; exit ${PIPESTATUS[0]}'
run behave_full       bash -c 'cd tests && behave --no-capture -f plain 2>&1 | tail -8; exit ${PIPESTATUS[0]}'
echo "=== post-run tree state"
git status --porcelain --untracked-files=all
echo "END"
