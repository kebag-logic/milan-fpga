# Reviewer toolchain environment: pinned RV32 SDK (archive sha256 matches scripts/ci_rv32_sdk.py) and GoogleTest/GMock 1.14.0.
P=<packet>
export MILAN_RV32_CC=$P/scratch/sdk/riscv32-ilp32d--glibc--stable-2025.08-1/bin/riscv32-linux-gcc
G=<googletest-1.14.0>
export PKG_CONFIG_PATH=$G/lib/pkgconfig CPLUS_INCLUDE_PATH=$G/include LIBRARY_PATH=$G/lib LD_LIBRARY_PATH=$G/lib
