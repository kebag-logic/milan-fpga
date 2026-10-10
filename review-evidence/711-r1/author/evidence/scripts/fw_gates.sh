#!/usr/bin/env bash
# Run rtl-fast's firmware-unit job steps from one checkout; one log and rc per step.
# Usage: fw_gates.sh SIDE CHECKOUT
set -u
side=$1; checkout=$2
out=$SCRATCH/fw/$side
mkdir -p "$out"
export TMPDIR=$SCRATCH/tmp PYTHONDONTWRITEBYTECODE=1
export MILAN_RV32_CC=$SDK/bin/riscv32-linux-gcc
cd "$checkout" || exit 2
step() {
  local name=$1; shift
  echo "== $name: $*" > "$out/$name.log"
  local t0=$SECONDS
  "$@" >> "$out/$name.log" 2>&1
  local rc=$?
  echo "$rc" > "$out/$name.rc"
  echo "$name rc=$rc seconds=$((SECONDS - t0))" >> "$out/summary.txt"
}
: > "$out/summary.txt"
step tally-selftest python3 sw/firmware/gtest/tally_selftest.py
step rv32-selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
step ctrl-firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir "$out/build"
step ctrl-nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4
step coverage-selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
step coverage-check python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4
echo "clean=$(git status --porcelain --untracked-files=all | wc -l)" >> "$out/summary.txt"
echo done >> "$out/summary.txt"
