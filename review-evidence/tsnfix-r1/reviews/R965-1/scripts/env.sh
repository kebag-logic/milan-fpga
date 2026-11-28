# Toolchain for the review runs: pinned GoogleTest/GMock 1.14.0 and clang-tidy 18.1.3, host gcc and clang.
# Usage: . env.sh PACKET_DIR   (PACKET_DIR/scratch/bin holds a clang-tidy link to the pinned 18.1.3 wrapper)
P=${1:?packet dir}
T=${TSN_TOOLS:?set TSN_TOOLS to the pinned toolchain directory (gtest-1.14.0, clang-18, clang-tidy-18)}
export PATH=$P/scratch/bin:/usr/local/bin:/usr/bin:/bin:$HOME/.local/bin
export PKG_CONFIG_PATH=$T/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$T/gtest-1.14.0 LD_LIBRARY_PATH=$T/gtest-1.14.0/lib
