# Source: toolchain environment for the round's runs (P is the packet root).
# GoogleTest 1.14.0 enters as a system include directory (CPLUS_INCLUDE_PATH), as the
# runner's /usr/include copy does, so its own headers raise no -Werror diagnostics.
export MILAN_RV32_CC="$P/scratch/sdk/bin/riscv32-linux-gcc"
G=$VALIDATION_TOOLS/gtest-1.14.0
export PKG_CONFIG_PATH=$G/lib/pkgconfig CMAKE_PREFIX_PATH=$G LD_LIBRARY_PATH=$G/lib
export CPLUS_INCLUDE_PATH=$G/include LIBRARY_PATH=$G/lib
export PATH=$VALIDATION_TOOLS/clang-18/bin:$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export TMPDIR="$P/scratch/tmp"
