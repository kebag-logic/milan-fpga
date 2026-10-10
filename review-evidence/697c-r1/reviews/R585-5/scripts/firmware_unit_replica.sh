#!/bin/bash
# Replay the firmware-unit job's firmware steps of .github/workflows/rtl-fast.yml
# (exact head) on a host checkout: each step under ctrl_capture.py into one
# capture, then the boundary step judging it. One log and rc file per step.
# Usage: firmware_unit_replica.sh TREE OUTDIR JOBS
# Env expected: MILAN_RV32_CC, PATH with clang 18 first, CPATH/LIBRARY_PATH/
# PKG_CONFIG_PATH/CMAKE_PREFIX_PATH for GoogleTest 1.14.0.
set -u
tree=$1; out=$2; jobs=$3
cap=$out/ctrl-capture
mkdir -p "$out"
cd "$tree" || exit 2
step() {  # name, command...
    name=$1; shift
    start=$(date +%s)
    "$@" > "$out/$name.log" 2>&1
    rc=$?
    echo "$rc $(( $(date +%s) - start ))s" > "$out/$name.rc"
    echo "$name rc=$rc $(( $(date +%s) - start ))s"
}
C="python3 sw/firmware/ctrl/test/ctrl_capture.py --out $cap --"
step 1-fw_rv32_selftest       $C python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
step 2-test_ctrl_firmware     $C python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs "$jobs"
step 3-test_ctrl_nvm          $C python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs "$jobs"
step 4-fw_coverage_selftest   $C python3 sw/firmware/gtest/fw_coverage.py --selftest
step 5-fw_coverage_check      $C python3 sw/firmware/gtest/fw_coverage.py --check --jobs "$jobs"
step 6-ctrl_boundary          python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --capture "$cap" --without verilator
echo done > "$out/ALL.done"
