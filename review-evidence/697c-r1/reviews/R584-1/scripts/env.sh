# Environment for the reviewer's local runs: the pinned RV32 SDK (installed by scripts/ci_rv32_sdk.py into
# scratch/rv32sdk), GoogleTest 1.14.0 under GTEST_PREFIX (as system headers), Verilator 5.050 at VERILATOR_BIN.
P="${PACKET:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
: "${GTEST_PREFIX:?set GTEST_PREFIX to a GoogleTest 1.14.0 install prefix}"
: "${VERILATOR_BIN:?set VERILATOR_BIN to the pinned Verilator 5.050 launcher}"
export MILAN_RV32_CC=$P/scratch/rv32sdk/bin/riscv32-linux-gcc
export CPLUS_INCLUDE_PATH=$GTEST_PREFIX/include
export LIBRARY_PATH=$GTEST_PREFIX/lib
export PKG_CONFIG_PATH=$GTEST_PREFIX/lib/pkgconfig
mkdir -p "$P/scratch/bin" && ln -sf "$VERILATOR_BIN" "$P/scratch/bin/verilator"
export PATH=$P/scratch/bin:$PATH
