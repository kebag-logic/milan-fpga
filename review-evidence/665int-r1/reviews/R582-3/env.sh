# Environment used by the R582-3 receipts (paths are this host's scratch).
export VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator
export MILAN_RV32_CC=$REVIEWS/665int-r582-3-packet/scratch/sdk/bin/riscv32-linux-gcc
export PKG_CONFIG_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$VALIDATION_TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib
export CPLUS_INCLUDE_PATH=$VALIDATION_TOOLS/gtest-1.14.0/include LIBRARY_PATH=$VALIDATION_TOOLS/gtest-1.14.0/lib
export PYTHONDONTWRITEBYTECODE=1
