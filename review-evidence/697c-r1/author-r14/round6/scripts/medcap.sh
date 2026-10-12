#!/usr/bin/env bash
# Scratch: two real builders, plain and under a capture, timed on four CPUs.
# usage: medcap.sh <tree> <capture> <log>
set -u
tree=$1; cap=$2; log=$3
export TMPDIR=$VALIDATION_STORAGE/697c-a583/tmpdir
export MILAN_RV32_CC=$VALIDATION_TOOLS/bootlin-504-probe/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc
cd "$tree" || exit 2
rm -rf "$cap"
{
for mode in plain capture; do
  for cmd in "sw/firmware/gtest/fw_rv32_selftest.py --require-rv32" "sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4"; do
    start=$(date +%s.%N)
    if [ $mode = plain ]; then taskset -c 124-127 python3 $cmd > /dev/null 2>&1; rc=$?
    else taskset -c 124-127 python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$cap" -- python3 $cmd > /dev/null 2>&1; rc=$?; fi
    end=$(date +%s.%N)
    echo "$mode rc=$rc $(echo "$end - $start" | bc) s: $cmd"
  done
done
} > "$log" 2>&1
