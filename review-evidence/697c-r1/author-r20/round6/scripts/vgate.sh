#!/usr/bin/env bash
# Scratch: the firmware-verilator job's gate command in one tree, timed.
# usage: vgate.sh <tree> <log> [taskset cpus]
set -u
tree=$1; log=$2; cpus=${3:-}
export TMPDIR=$VALIDATION_STORAGE/697c-a583/tmpdir VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator VERILATOR_JOBS=2
export MILAN_RV32_CC=$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc
cd "$tree" || exit 2
git clean -fdxq tb/verilator/mbx
start=$(date +%s.%N)
if [ -n "$cpus" ]; then taskset -c "$cpus" python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator > "$log" 2>&1
else python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator > "$log" 2>&1; fi
rc=$?
end=$(date +%s.%N)
echo "rc=$rc $(echo "$end - $start" | bc) s" >> "$log"
