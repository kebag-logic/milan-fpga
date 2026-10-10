# Reviewer toolchain environment. Set P to the packet directory and TOOLS to the toolchain directory first.
# Pinned RV32 SDK (archive sha256 d42680e9... equals scripts/ci_rv32_sdk.py ARCHIVE_SHA256), extracted under
# $P/scratch/sdk; GoogleTest/GMock 1.14.0; pinned Verilator 5.050.
export MILAN_RV32_CC=$P/scratch/sdk/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc
G=$TOOLS/gtest-1.14.0
export PKG_CONFIG_PATH=$G/lib/pkgconfig CPLUS_INCLUDE_PATH=$G/include LIBRARY_PATH=$G/lib LD_LIBRARY_PATH=$G/lib
export PATH=$TOOLS/pinned-verilator-5.050:$PATH
