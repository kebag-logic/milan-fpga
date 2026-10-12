#!/usr/bin/env bash
# Scratch: the firmware-unit job's boundary step in one tree against one capture, timed, on given CPUs.
# usage: hgate.sh <tree> <capture> <log> <cpus> [python]
set -u
tree=$1; cap=$2; log=$3; cpus=$4; py=${5:-python3}
export TMPDIR=$VALIDATION_STORAGE/697c-a583/tmpdir
export MILAN_RV32_CC=$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc
cd "$tree" || exit 2
uptime > "$log.uptime"
start=$(date +%s.%N)
taskset -c "$cpus" "$py" sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --capture "$cap" --without verilator > "$log" 2>&1
rc=$?
end=$(date +%s.%N)
uptime >> "$log.uptime"
echo "rc=$rc $(echo "$end - $start" | bc) s" >> "$log"
