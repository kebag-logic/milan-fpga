#!/usr/bin/env bash
# Start the composed firmware gates detached, one log and rc file each.
# Usage: run_firmware.sh <clone> <outdir> <rv32-cc> <gtest-prefix>
set -u
clone=$1; out=$2; cc=$3; gt=$4
mkdir -p "$out"
export PYTHONDONTWRITEBYTECODE=1 MILAN_RV32_CC="$cc"
export PKG_CONFIG_PATH="$gt/lib/pkgconfig" CPLUS_INCLUDE_PATH="$gt/include" \
       LIBRARY_PATH="$gt/lib" LD_LIBRARY_PATH="$gt/lib"
cd "$clone" || exit 2
start() {
  name=$1; shift
  setsid nohup bash -c 's=$(date +%s); "$@" >"$0.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s)-s ))s" >"$0.rc"' \
    "$out/$name" "$@" </dev/null >/dev/null 2>&1 &
}
start ctrl_nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 5
start fw_coverage python3 sw/firmware/gtest/fw_coverage.py --check --jobs 5
start ctrl_fw python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --jobs 4
echo started
