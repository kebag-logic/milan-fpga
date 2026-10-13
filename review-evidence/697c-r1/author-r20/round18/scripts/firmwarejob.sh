#!/usr/bin/env bash
# Scratch: one of rtl-fast.yml's four firmware jobs, its commands after the setup steps (apt, cache, SDK download),
# as the workflow runs them, each timed, one log each.
# usage: firmwarejob.sh <tree> <log directory> <unit|control|aecp|srp>
set -u
tree=$1; logs=$2; job=$3
mkdir -p "$logs"
cd "$tree" || exit 2
total=$SECONDS
step() { local name=$1; shift; local start=$SECONDS; "$@" > "$logs/$name.log" 2>&1; local rc=$?
  echo "rc=$rc $((SECONDS - start)) s $name: $*"; }
echo "nproc=$(nproc) $(date -u +%FT%TZ) $(git log --oneline -1 | cut -c1-12)"
case $job in
  unit)
    step tally python3 sw/firmware/gtest/tally_selftest.py
    step sdk-selftest python3 scripts/ci_rv32_sdk_selftest.py
    step rv32-selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
    step ctrl-firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard 0/4
    step ctrl-nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs "$(nproc)"
    step coverage-selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
    step coverage-check python3 sw/firmware/gtest/fw_coverage.py --check --jobs "$(nproc)";;
  control|aecp|srp)
    shard=$(case $job in control) echo 1;; aecp) echo 2;; srp) echo 3;; esac)
    step sdk-selftest python3 scripts/ci_rv32_sdk_selftest.py
    step "ctrl-firmware-$job" python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --shard "$shard/4";;
  *) echo "unknown job $job"; exit 2;;
esac
echo "total $((SECONDS - total)) s $(date -u +%FT%TZ)"
