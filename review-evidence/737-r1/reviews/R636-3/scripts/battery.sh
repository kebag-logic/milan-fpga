#!/usr/bin/env bash
# Run the round-3 CI control battery against one disposable copy of the exact head.
# Usage: battery.sh <copy-dir> <log-dir>
# Each control runs in the background with its own log and rc file; the caller
# waits on the rc files in the foreground.
set -u
copy="$1"; logs="$2"
mkdir -p "$logs"
cd "$copy" || exit 2
run() {
  local name="$1"; shift
  ( start=$(date +%s.%N)
    "$@" > "$logs/$name.log" 2>&1
    rc=$?
    end=$(date +%s.%N)
    printf '%s %s\n' "$rc" "$(echo "$end - $start" | bc)" > "$logs/$name.rc" ) &
}
run gate-check        python3 scripts/ci_gate_workflows.py --check
run gate-selftest     python3 scripts/ci_gate_workflows_selftest.py
run fail-fast         python3 scripts/ci_fail_fast_selftest.py
run runtime-evidence  python3 scripts/ci_runtime_evidence_selftest.py
run manifest          python3 scripts/ci_manifest_selftest.py
run case-receipts     python3 scripts/ci_case_receipts_selftest.py
run workflow-plan     python3 scripts/ci_workflow_plan_selftest.py
run evidence-pins     python3 scripts/generate_ci_evidence_pins.py --check
run suite-pieces      python3 scripts/ci_suite_pieces_selftest.py
run suite-collect     python3 scripts/ci_suite_collect_selftest.py
run events-check      python3 scripts/ci_events.py --check
run events-selftest   python3 scripts/ci_events.py --selftest
run baremetal         python3 scripts/check_baremetal_only.py
run docs-check        python3 scripts/docs_check.py
run doc-paths         python3 scripts/check_doc_paths.py
wait
