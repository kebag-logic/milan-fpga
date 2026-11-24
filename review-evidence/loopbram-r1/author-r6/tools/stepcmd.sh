#!/bin/bash
# stepcmd.sh <checkout> <runner-temp> <log> <command...>: run one command of a docs.yml step
# with the environment wfreplay.py gives that step (same shim, RUNNER_TEMP and job budgets).
# Used for a step whose commands together exceed one foreground call; the step's outcome
# is success only when each of its commands, run in order with one RUNNER_TEMP, exits 0.
set -u
checkout=$1 temp=$2 log=$3
shift 3
shim=$(dirname "$(readlink -f "$0")")/../scratch/docswf2/shim
mkdir -p "$temp"
cd "$checkout" || exit 2
env PATH="$shim:/usr/local/bin:/usr/bin:/bin" RUNNER_TEMP="$temp" TMPDIR="$temp" GITHUB_WORKSPACE="$checkout" \
  GITHUB_SHA="$(git rev-parse HEAD)" PYTHONDONTWRITEBYTECODE=1 CI_BUILD_JOBS=4 CI_TOOL_BUILD_JOBS=4 \
  CI_CAMPAIGN_JOBS=4 VERILATOR_JOBS=4 SIM_JOBS=4 MAKEFLAGS="-j1 --no-print-directory" \
  bash --noprofile --norc -eo pipefail -c "$*" >> "$log" 2>&1
rc=$?
echo "command: $* -> exit $rc" | tee -a "$log"
exit $rc
