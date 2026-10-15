#!/usr/bin/env bash
# Revert scripts/ci_suite_workflows.py to the round-4 literal matching (08adb21a)
# in a disposable copy of the head, regenerate the workflows with it, and run
# the committed gates that hold the generator. A gate that still passes does not
# guard the merge's derived arm/--expect replacement.
# Usage: revert_generator_probe.sh <repo-clone> <scratch-dir>
set -u
repo=$1; d=$2/revert-generator
rm -rf "$d"; mkdir -p "$d"
git -C "$repo" archive HEAD | tar -x -C "$d"
for sm in third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack; do
  rmdir "$d/$sm" 2>/dev/null; ln -s "$(cd "$repo/$sm" && pwd)" "$d/$sm"
done
git -C "$repo" show 08adb21af:scripts/ci_suite_workflows.py > "$d/scripts/ci_suite_workflows.py"
cd "$d"
python3 scripts/ci_gate_workflows.py; echo "regenerate rc=$?"
echo "stray arm lines in generated rtl.yml: $(grep -c ') test "$(cat "$RUNNER_TEMP/owned-suites")" = milan_dp' .github/workflows/rtl.yml)"
echo "generated --require-target-sha expectation: $(grep -o -- '--require-target-sha --expect [0-9]*' .github/workflows/rtl.yml | sort | uniq -c | tr '\n' ' ')"
for g in "python3 scripts/ci_gate_workflows.py --check" "python3 scripts/ci_events.py --check" \
         "python3 scripts/ci_gate_workflows_selftest.py" "python3 scripts/ci_suite_pieces_selftest.py" \
         "python3 scripts/ci_suite_collect_selftest.py" "python3 scripts/suite_shards.py --selftest" \
         "python3 scripts/ci_workflow_plan_selftest.py" "python3 scripts/ci_runtime_evidence_selftest.py"; do
  $g > /dev/null 2>&1; echo "rc=$? $g"
done
