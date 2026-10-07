#!/usr/bin/env bash
# R524-3: launch the round-3 firmware gates concurrently at the exact head.
# Usage: run_gates.sh <clone> <packet> <rv32-gcc>
# Each gate writes receipts/gate-<name>.log and receipts/gate-<name>.rc.
set -u
CLONE=$1 PACKET=$2 CC=$3
R=$PACKET/receipts
export MILAN_RV32_CC=$CC TMPDIR=$PACKET/scratch/tmp PYTHONDONTWRITEBYTECODE=1
mkdir -p "$TMPDIR"
cd "$CLONE" || exit 2
launch() {
  local name=$1; shift
  ( "$@" > "$R/gate-$name.log" 2>&1; echo $? > "$R/gate-$name.rc" ) &
  echo "$!" > "$R/gate-$name.pid"
}
launch ctrl      python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
launch nvm       python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4
launch rv32self  python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
launch coverage  python3 sw/firmware/gtest/fw_coverage.py --check --jobs 3
launch covself   python3 sw/firmware/gtest/fw_coverage.py --selftest
launch tally     python3 sw/firmware/gtest/tally_selftest.py --mutants
