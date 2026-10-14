#!/bin/bash
set -euo pipefail
export GITHUB_ENV=/scratch/job.env
finish() {
 rc=$?
 cat /sys/fs/cgroup/memory.peak > /scratch/memory.peak
 cat /sys/fs/cgroup/memory.events > /scratch/memory.events
 printf '%s\n' "$rc" > /scratch/result.rc
 date +%s.%N > /scratch/finished
 exit "$rc"
}
trap finish EXIT
date +%s.%N > /scratch/started
set -euo pipefail
cpus="$(nproc)"
test "$cpus" -gt 0
campaign=$(( cpus < 4 ? cpus : 4 ))
simulations=$(( cpus < 4 ? cpus : 4 ))
{
  printf 'CI_BUILD_JOBS=%s\n' "$cpus"
  printf 'CI_CAMPAIGN_JOBS=%s\n' "$campaign"
  printf 'VERILATOR_JOBS=%s\n' "$cpus"
  printf 'SIM_JOBS=%s\n' "$simulations"
  printf 'MAKEFLAGS=-j1 --no-print-directory\n'
} >> "$GITHUB_ENV"

while IFS= read -r assignment; do export "$assignment"; done < "$GITHUB_ENV"
nproc > /scratch/cpus
export VERILATOR_JOBS=$(( CI_BUILD_JOBS / CI_CAMPAIGN_JOBS ))
python3 tb/verilator/capture_coherence/mutants.py --whole-suite --jobs "$CI_CAMPAIGN_JOBS"
