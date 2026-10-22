#!/usr/bin/env bash
# firmware_gates.sh OUTDIR: the local firmware gate set of CI_WORKFLOWS.md
# ("Local commands", firmware block) plus the hosted firmware-unit job's RV32
# self-test and the shard and census checks, in order, each with its own log,
# rc and wall seconds. Pinned GoogleTest 1.14.0 and Clang 18 (the stack's
# gates refuse the host's), the pinned Verilator, and the verified RV32 SDK
# selected through MILAN_RV32_CC.
set -u
out="$1"
mkdir -p "$out"
source $VALIDATION_STORAGE/scratch/a662/env.sh
export MILAN_RV32_CC=$VALIDATION_STORAGE/771-a662-r2/rv32-sdk/host/bin/riscv32-linux-gcc
export PKG_CONFIG_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib/pkgconfig
export CMAKE_PREFIX_PATH=$VALIDATION_TOOLS/gtest-1.14.0
export LD_LIBRARY_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib
export PATH=$VALIDATION_TOOLS/clang-18/bin:$PATH
unset MAKEFLAGS
cd $LANES/771-pin4 || exit 2
LW=$LANES/771-pin4/third_party/lwSRP
{
    echo "head=$(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l)"
    echo "MILAN_RV32_CC=$MILAN_RV32_CC"
    readlink -f "$MILAN_RV32_CC"
    "$MILAN_RV32_CC" --version | head -n 1
    sha256sum "$(dirname "$MILAN_RV32_CC")/riscv32-buildroot-linux-gnu-gcc.br_real"
    python3 scripts/ci_rv32_sdk.py --destination "$(dirname "$(dirname "$MILAN_RV32_CC")")" --verify-only 2>&1 | tail -n 2
    gcc --version | head -n 1; g++ --version | head -n 1; clang --version | head -n 1
    echo "gtest $(pkg-config --modversion gtest) gmock $(pkg-config --modversion gmock)"
    "$VERILATOR" --version
    make --version | head -n 1
    date -Is
} > "$out/env.txt" 2>&1
run() {
    local name="$1"; shift
    local t0=$SECONDS
    echo "$(date -Is) start $name: $*" >> "$out/progress.txt"
    "$@" > "$out/$name.log" 2>&1
    local rc=$?
    echo "$rc" > "$out/$name.rc"
    echo "$((SECONDS - t0))" > "$out/$name.seconds"
    echo "$(date -Is) end $name rc=$rc $((SECONDS - t0))s" >> "$out/progress.txt"
}
run fw_rv32_selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
run tally_selftest_mutants python3 sw/firmware/gtest/tally_selftest.py --mutants
run ctrl_firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp "$LW" --jobs 4
run ctrl_firmware_shards python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
run firmware_census python3 scripts/ci_events.py --firmware-census
run ctrl_nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4
run fw_coverage_selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
run fw_coverage_check python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp "$LW" --jobs 4
run ctrl_boundary python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
echo "head_after=$(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l)" >> "$out/env.txt"
date -Is > "$out/done"
