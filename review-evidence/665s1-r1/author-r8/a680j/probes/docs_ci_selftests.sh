#!/usr/bin/env bash
# The docs workflow's CI-tooling self-tests and checks (docs-gates-0 and docs-gates-2) that run without a
# runner install or network, for the CI scripts the merge brings in; prints each command's exit status
# and a total. Run from the repository root given as $1.
set -u
cd "$1" || exit 2
failed=0
run() {
    "$@"
    local rc=$?
    echo "[rc=$rc] $*"
    [ "$rc" -eq 0 ] || failed=$((failed + 1))
}
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
run python3 scripts/ci_events.py --selftest
run python3 scripts/act_ci.py --selftest
run python3 sw/builder/test_firmware_compiler.py --selftest
echo "docs CI self-tests: $failed failed"
exit $((failed > 0))
