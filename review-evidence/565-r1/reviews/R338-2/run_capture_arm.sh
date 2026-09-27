#!/bin/bash
# Reproduce one capture arm at the reviewed head, offline, in a user+net namespace, on 8 CPUs.
# Usage: run_capture_arm.sh <repo> <sdk-dir> <litex-venv-python> <shape-suffix> <cpu-hz> <on|off> <build-dir> <log>
set -u
repo=$1 sdk=$2 py=$3 shape=$4 hz=$5 traffic=$6 build=$7 log=$8
cd "$repo" || exit 2
export PATH="$(dirname "$py"):$sdk/bin:$PATH" LITEX_ENV_CC_TRIPLE=riscv32-linux PYTHONHASHSEED=0 \
       COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
{ echo "START $(date -u +%FT%TZ) head=$(git rev-parse HEAD) verilator=$(verilator --version) cc=$(riscv32-linux-gcc -dumpversion)"
  taskset -c 0-7 unshare -Urn "$py" -B tb/verilator/nvm_capture_cpu/run.py --shape "endstation_ax7101_$shape" \
    --cpu-hz "$hz" --captures 16 --traffic "$traffic" --build-dir "$build"
  echo "RC=$? END $(date -u +%FT%TZ)"; } > "$log" 2>&1
