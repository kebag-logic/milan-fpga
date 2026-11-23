#!/usr/bin/env bash
# The 28 CI and docs gates of round 1, run in order from the lane checkout.
# Usage: run_gates.sh CHECKOUT BASE MARKDOWN_PYTHON
set -uo pipefail
cd "$1" || exit 2
base="$2"
md="$3"
git rev-parse HEAD
status=0
run() {
  local rc
  "$@" > /tmp/a827-r2-gate.out 2>&1
  rc=$?
  echo "== rc=$rc $*"
  tail -n 2 /tmp/a827-r2-gate.out
  [ "$rc" -eq 0 ] || status=1
}
run python3 scripts/ci_gate_workflows.py --check
run python3 scripts/ci_events.py --check
run python3 scripts/ci_gate_workflows_selftest.py
run python3 scripts/ci_case_receipts_selftest.py
run python3 scripts/ci_make_cases_selftest.py
run python3 scripts/ci_maap_cases_selftest.py
run python3 scripts/ci_capture_cases_selftest.py
run python3 scripts/ci_suite_pieces_selftest.py
run python3 scripts/ci_suite_collect_selftest.py
run python3 scripts/ci_fail_fast_selftest.py
run python3 scripts/ci_runtime_evidence_selftest.py
run python3 scripts/ci_install_cache_selftest.py
run python3 scripts/generate_ci_evidence_pins.py --check
run python3 scripts/ci_workflow_plan_selftest.py
run python3 scripts/ci_manifest_selftest.py
run python3 scripts/check_wire_accountability.py --self-test
run python3 scripts/docs_check.py
run python3 scripts/check_doc_paths.py
run python3 scripts/check_doc_style.py
run python3 scripts/check_doc_style.py --selftest
run "$md" scripts/check_em_dash.py --base "$base"
run python3 scripts/check_hygiene.py --check
run python3 scripts/check_todo_ownership.py
run python3 scripts/check_sh_idiom.py
run python3 scripts/check_py_idiom.py
run python3 scripts/check_py_idiom.py --selftest
run python3 scripts/docs_inventory.py --check
run python3 scripts/act_ci.py --selftest
echo "== overall status=$status"
exit "$status"
