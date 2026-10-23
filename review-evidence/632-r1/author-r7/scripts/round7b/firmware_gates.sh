#!/usr/bin/env bash
# Round 7b: the local firmware gate set of docs/testing/CI_WORKFLOWS.md (the
# firmware block: tally mutants, the control firmware with its RV32 self-test
# against the pinned lwSRP, the boundary, the NVM control firmware, the
# coverage self-test and check), plus the RV32 harness self-test and the shard
# check of the hosted control phases, in a clean clone at <rev>, each with its
# own log, rc and wall seconds. --jobs 4 where the block says 16 (this lane's
# limit). Pinned GoogleTest 1.14.0 and Clang 18 (the stack's gates refuse the
# host's), the pinned Verilator, the verified RV32 SDK through MILAN_RV32_CC.
# The boundary gate runs under the LiteX interpreter: its sw/litex arm imports
# migen, which the hosted job installs from sw/litex/litex_pins.txt first.
# usage: firmware_gates.sh <clone> <out> [all|nb|boundary]  (nb: all but the boundary gate)
set -u
C=$1; out=$2; mode=${3:-all}
mkdir -p "$out"
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export PATH=$VALIDATION_STORAGE/scratch/632-a659/r7b/clang18bin:$VALIDATION_STORAGE/scratch/632-a659/r7/make43/bin:$VALIDATION_TOOLS/sv2v-v0.0.12:$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export MILAN_RV32_CC=$VALIDATION_STORAGE/scratch/632-a659/r7<home-path>/host/bin/riscv32-linux-gcc
export PKG_CONFIG_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib/pkgconfig
export CMAKE_PREFIX_PATH=$VALIDATION_TOOLS/gtest-1.14.0
export LD_LIBRARY_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib
export VERILATOR_JOBS=2 PYTHONHASHSEED=0
unset MAKEFLAGS
LITEX_PY=$WORKSPACE_HOME/litex-milan/venv/bin/python3
cd "$C" || exit 2
LW=$C/third_party/lwSRP
{
    echo "head=$(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l)"
    git submodule status
    echo "MILAN_RV32_CC=$MILAN_RV32_CC"
    "$MILAN_RV32_CC" --version | head -n 1
    python3 scripts/ci_rv32_sdk.py --destination "$(dirname "$(dirname "$MILAN_RV32_CC")")" --verify-only 2>&1 | tail -n 2
    gcc --version | head -n 1; g++ --version | head -n 1; clang --version | head -n 1; clang-18 --version | head -n 1
    echo "gtest $(pkg-config --modversion gtest) gmock $(pkg-config --modversion gmock)"
    "$VERILATOR" --version
    make --version | head -n 1
    python3 --version; "$LITEX_PY" --version
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
if [ "$mode" != boundary ]; then
run fw_rv32_selftest python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32
run tally_selftest_mutants python3 sw/firmware/gtest/tally_selftest.py --mutants
run ctrl_firmware python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp "$LW" --jobs 4
run ctrl_firmware_shards python3 sw/firmware/ctrl/test/test_ctrl_firmware_shards.py
run ctrl_nvm python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4
run fw_coverage_selftest python3 sw/firmware/gtest/fw_coverage.py --selftest
run fw_coverage_check python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp "$LW" --jobs 4
fi
[ "$mode" != nb ] && run ctrl_boundary "$LITEX_PY" sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest
echo "head_after=$(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l)" >> "$out/env.txt"
date -Is > "$out/done-$mode"
