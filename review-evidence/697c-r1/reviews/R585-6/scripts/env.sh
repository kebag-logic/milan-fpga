# Reviewer environment: pinned GoogleTest 1.14.0, Clang 18, pinned RV32 SDK, pinned Verilator 5.050.
P=$REVIEWS/697c-r585-6-packet
G=$VALIDATION_TOOLS/gtest-1.14.0
export PKG_CONFIG_PATH=$G/lib/pkgconfig CMAKE_PREFIX_PATH=$G LD_LIBRARY_PATH=$G/lib
export CPLUS_INCLUDE_PATH=$G/include C_INCLUDE_PATH=$G/include LIBRARY_PATH=$G/lib
export MILAN_RV32_CC=$P/scratch/sdk/bin/riscv32-linux-gcc
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export TMPDIR=$P/scratch/tmp
mkdir -p $TMPDIR
