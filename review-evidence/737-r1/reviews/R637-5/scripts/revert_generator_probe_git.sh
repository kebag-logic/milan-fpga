#!/usr/bin/env bash
# Git-backed variant of revert_generator_probe.sh: some committed self-tests read
# HEAD, so run every "CI scheduling and evidence controls" command plus the
# CI-event check/self-test in a disposable shared clone at the exact head with
# scripts/ci_suite_workflows.py reverted to 08adb21a and workflows regenerated.
# Nothing is committed. Usage: revert_generator_probe_git.sh <repo-clone> <scratch-dir>
set -u
repo=$(cd "$1" && pwd); d=$2/revert-git; logs=$2/revert-logs
rm -rf "$d" "$logs"; mkdir -p "$logs"
git clone -q --shared --no-checkout "$repo" "$d"
cd "$d" && git checkout -q --detach e3d25d964b5bbf0187290d0a357c6a6e4c5afd17
for sm in third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack; do
  rmdir "$sm" 2>/dev/null; ln -s "$repo/$sm" "$sm"
done
git show 08adb21af:scripts/ci_suite_workflows.py > scripts/ci_suite_workflows.py
python3 scripts/ci_gate_workflows.py
echo "stray arm lines: $(grep -c ') test "$(cat "$RUNNER_TEMP/owned-suites")" = milan_dp' .github/workflows/rtl.yml)"
for g in "scripts/ci_gate_workflows.py --check" scripts/ci_gate_workflows_selftest.py scripts/ci_case_receipts_selftest.py \
  scripts/ci_make_cases_selftest.py scripts/ci_maap_cases_selftest.py scripts/ci_capture_cases_selftest.py \
  scripts/ci_suite_pieces_selftest.py scripts/ci_suite_collect_selftest.py scripts/ci_fail_fast_selftest.py \
  scripts/ci_runtime_evidence_selftest.py scripts/ci_install_cache_selftest.py "scripts/generate_ci_evidence_pins.py --check" \
  scripts/ci_workflow_plan_selftest.py scripts/ci_manifest_selftest.py "scripts/ci_events.py --check" \
  "scripts/ci_events.py --selftest" "scripts/suite_shards.py --selftest" scripts/suite_tally_selftest.py; do
  n=$(echo "$g" | tr ' /' '__')
  ( python3 $g > "$logs/$n.log" 2>&1; echo "rc=$? python3 $g" > "$logs/$n.rc" ) &
done
wait; cat "$logs"/*.rc
