#!/usr/bin/env bash
# Scratch: firmware-unit's steps after its setup, as rtl-fast.yml runs them (no capture), each timed, one log each.
# usage: unitjob.sh <tree> <log directory>
set -u
tree=$1; logs=$2
mkdir -p "$logs"
cd "$tree" || exit 2
total=$SECONDS
step() { local name=$1; shift; local start=$SECONDS; "$@" > "$logs/$name.log" 2>&1; local rc=$?
  echo "rc=$rc $((SECONDS - start)) s $name: $*"; }
echo "nproc=$(nproc) $(date -u +%FT%TZ)"
step tally python3 sw/firmware/gtest/tally_selftest.py
step rv32-selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
step ctrl-firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
step ctrl-nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs "$(nproc)"
step coverage-selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
step coverage-check python3 sw/firmware/gtest/fw_coverage.py --check --jobs "$(nproc)"
echo "total $((SECONDS - total)) s $(date -u +%FT%TZ)"
