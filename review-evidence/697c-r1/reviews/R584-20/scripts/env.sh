# Environment for the R584-20 composition probes. Source it with PACKET (this packet's
# directory) and TOOLS (a directory holding gtest-1.14.0) set. PACKET/scratch/bin holds
# clang, clang-18 and clang++ wrappers around a Clang 18.1.3 (Ubuntu 24.04 package) root.
# PACKET/scratch/rv32/host is the pinned RV32 SDK installed by scripts/ci_rv32_sdk.py (digest
# d42680e9...), and PACKET/scratch/venv312 a CPython 3.12.3 venv with pyyaml,
# sw/litex/litex_pins.txt and tools/markdown/requirements.txt installed.
: "${PACKET:?set PACKET to the review packet directory}"
: "${TOOLS:?set TOOLS to the directory holding gtest-1.14.0 and clang-18}"
export MILAN_RV32_CC="$PACKET/scratch/rv32/host/bin/riscv32-linux-gcc"
export PATH="$PACKET/scratch/venv312/bin:$PACKET/scratch/bin:$PATH"
export CPLUS_INCLUDE_PATH="$TOOLS/gtest-1.14.0/include"
export LIBRARY_PATH="$TOOLS/gtest-1.14.0/lib"
export LD_LIBRARY_PATH="$TOOLS/gtest-1.14.0/lib"
export PKG_CONFIG_PATH="$TOOLS/gtest-1.14.0/lib/pkgconfig"
export CMAKE_PREFIX_PATH="$TOOLS/gtest-1.14.0"
export PYTHONDONTWRITEBYTECODE=1
export LC_ALL=C
