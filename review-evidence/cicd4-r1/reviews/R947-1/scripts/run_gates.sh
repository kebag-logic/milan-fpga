#!/usr/bin/env bash
# Run the gates this change touches, concurrently, each with its own log and rc file.
# Usage: run_gates.sh <checkout> <output-dir>
set -uo pipefail
repo="$1"; out="$2"
mkdir -p "$out"
cd "$repo" || exit 2
run() {  # name, command...
  local name="$1"; shift
  ( start=$(date +%s); "$@" >"$out/$name.log" 2>&1; rc=$?
    echo "$rc $(( $(date +%s) - start ))s" >"$out/$name.rc" ) &
}
run gate_workflows_check      python3 scripts/ci_gate_workflows.py --check
run gate_workflows_selftest   python3 scripts/ci_gate_workflows_selftest.py
run fast_legs_selftest        bash -c 'cd scripts && python3 ci_fast_legs_selftest.py'
run fast_tool_selftest        bash -c 'cd scripts && python3 ci_fast_tool_selftest.py'
run events_check              python3 scripts/ci_events.py --check
run events_selftest           python3 scripts/ci_events.py --selftest
run ctrl_firmware_shards      python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
run suite_shards_selftest     python3 scripts/suite_shards.py --selftest
run fail_fast_selftest        python3 scripts/ci_fail_fast_selftest.py
run runtime_evidence_selftest python3 scripts/ci_runtime_evidence_selftest.py
run workflow_plan_selftest    python3 scripts/ci_workflow_plan_selftest.py
run manifest_selftest         python3 scripts/ci_manifest_selftest.py
run evidence_pins_check       python3 scripts/generate_ci_evidence_pins.py --check
run docs_check                python3 scripts/docs_check.py
run py_idiom                  python3 scripts/check_py_idiom.py
wait
for f in "$out"/*.rc; do printf '%-28s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done | tee "$out/summary"
