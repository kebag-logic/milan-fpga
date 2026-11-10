#!/usr/bin/env bash
# litex_sims_diag.sh: elaborate-gates-1's gate_19 run again in that job's own worktree and environment (its HOME,
# RUNNER_TEMP, GITHUB_ENV and GITHUB_PATH as the replay gave them), with one change: LITEX_SIM_TIMEOUT=7200 in place
# of the default 900 s, because test_soc_timing_cuts hit 900 s three times under host load (diagnostic only)
J=/data-2/milan/tmp/665s7-a757c/ci/2128daad26b9/jobs/elaborate__elaborate-gates-1
cd $J/wt
set -a; . $J/github_env; set +a
export HOME=$J/home RUNNER_TEMP=$J/temp TMPDIR=$J/tmp LITEX_SIM_TIMEOUT=7200
export PATH=$(paste -sd: $J/github_path):$VALIDATION_TOOLS/pinned-verilator-5.050:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_STORAGE/scratch/a662/make43/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
git rev-parse HEAD
start=$(date +%s)
bash --noprofile --norc -eo pipefail -c 'scripts/run_litex_sims.sh "$RUNNER_TEMP/litex-sim-logs-diag"'
rc=$?
echo "wall $(( $(date +%s) - start )) s"
echo "rc=$rc"
