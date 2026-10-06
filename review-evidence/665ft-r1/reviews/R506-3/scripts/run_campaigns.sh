#!/usr/bin/env bash
# Launch the round-3 gate campaigns concurrently from the exact-head clone.
# Usage: run_campaigns.sh <clone> <packet>
set -u
C=$1; P=$2
export TMPDIR=$P/scratch/tmp
mkdir -p "$TMPDIR" "$P/receipts"
cd "$C" || exit 2
run() { name=$1; shift; ( "$@" > "$P/receipts/$name.log" 2>&1; echo $? > "$P/receipts/$name.rc" ) & }
run tally_selftest_mutants python3 sw/firmware/gtest/tally_selftest.py --mutants
run ctrl_nvm_selftest python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --self-test --jobs 7
run fw_coverage_check python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
run fw_coverage_selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
run ctrl_fw_selftest python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --self-test
wait
