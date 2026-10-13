#!/usr/bin/env bash
# Scratch: the firmware gates of one tree in the CI-parity container, one log per command.
# usage: container-gates.sh <tree> <log directory>
set -u
tree=$1; logs=$2
mkdir -p "$logs"
run() { # name command...
  local name=$1; shift
  { date -u +%FT%TZ; $VALIDATION_STORAGE/697c-a583/scripts/inbox.sh "$tree" "$@"; echo "rc=$?"; date -u +%FT%TZ; } > "$logs/$name.log" 2>&1
}
run versions bash -c 'python3 --version; gcc --version | head -1; gcov --version | head -1; dpkg -l libgtest-dev | tail -1'
run fw-rv32-selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
run tally-selftest python3 sw/firmware/gtest/tally_selftest.py
run fw-gate python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4
run coverage-selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
run coverage-check python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
run ctrl-image-selftest python3 sw/firmware/ctrl/test/ctrl_image_selftest.py --require-rv32
echo done > "$logs/DONE"
