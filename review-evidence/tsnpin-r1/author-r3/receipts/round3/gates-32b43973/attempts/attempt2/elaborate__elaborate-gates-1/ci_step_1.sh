set -euo pipefail
cpus="$(nproc)"
test "$cpus" -gt 0
campaign=$(( cpus < 4 ? cpus : 4 ))
simulations=$(( cpus < 4 ? cpus : 4 ))
tool_build=$(( cpus < 8 ? cpus : 8 ))
{
  printf 'CI_BUILD_JOBS=%s\n' "$cpus"
  printf 'CI_TOOL_BUILD_JOBS=%s\n' "$tool_build"
  printf 'CI_CAMPAIGN_JOBS=%s\n' "$campaign"
  printf 'VERILATOR_JOBS=%s\n' "$cpus"
  printf 'SIM_JOBS=%s\n' "$simulations"
  printf 'MAKEFLAGS=-j1 --no-print-directory\n'
} >> "$GITHUB_ENV"
