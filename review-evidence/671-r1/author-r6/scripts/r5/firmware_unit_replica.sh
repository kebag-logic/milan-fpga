#!/usr/bin/env bash
# Local replica of .github/workflows/rtl-fast.yml job firmware-unit at the
# checked-out head, one rc line per command. Install steps are omitted (the
# pinned RV32 SDK is already at ~/br-milan-rv32/host; GoogleTest is the
# distribution's). Usage: firmware_unit_replica.sh <repo> <python> <logdir> <jobs>
set -u
repo=$1; py=$2; logs=$3; jobs=$4
mkdir -p "$logs"
cd "$repo" || exit 2
n=0; fails=0
step() {
  n=$((n + 1))
  local log; log=$(printf '%s/%02d.log' "$logs" "$n")
  "$@" > "$log" 2>&1
  local rc=$?
  [ "$rc" -eq 0 ] || fails=$((fails + 1))
  printf 'rc=%d  %s\n' "$rc" "$*"
}
step "$py" sw/firmware/gtest/tally_selftest.py
step "$py" scripts/ci_rv32_sdk_selftest.py
step "$py" sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
step "$py" sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs "$jobs"
step "$py" sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs "$jobs"
step "$py" sw/firmware/gtest/fw_coverage.py --selftest
step "$py" sw/firmware/gtest/fw_coverage.py --check --jobs "$jobs"
echo "steps: $n  failing: $fails"
[ "$fails" -eq 0 ]
