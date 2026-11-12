#!/bin/bash
# Run listed docs-gates-0 run steps from the repo root; one log and rc per step.
# usage: run_gates.sh <repo> <step-dir> <out-dir> <runner-temp> <step numbers...>
repo=$1; steps=$2; out=$3; export RUNNER_TEMP=$4; shift 4
cd "$repo" || exit 9
export EVENT_NAME=push PUSH_BEFORE_SHA=1d6bf555d6c1 CI_BUILD_JOBS=16 CI_TOOL_BUILD_JOBS=8 CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=16 SIM_JOBS=4 MAKEFLAGS="-j1 --no-print-directory"
for n in "$@"; do
  f="$steps/$n.sh"; [ -f "$f" ] || continue
  bash -eo pipefail "$f" > "$out/step$n.log" 2>&1; echo $? > "$out/step$n.rc"
done
