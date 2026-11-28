# Source before the gate runs: pinned GoogleTest 1.14.0, clang-18 (compiler-token gate) and clang-tidy 18.1.3.
# TOOLS: directory holding gtest-1.14.0, clang-18/bin and clang-tidy-18/bin.
: "${TOOLS:?set TOOLS to the pinned toolchain directory}"
export PATH="$TOOLS/clang-tidy-18/bin:$TOOLS/clang-18/bin:$PATH"
export PKG_CONFIG_PATH="$TOOLS/gtest-1.14.0/lib/pkgconfig"
export CMAKE_PREFIX_PATH="$TOOLS/gtest-1.14.0"
export LD_LIBRARY_PATH="$TOOLS/gtest-1.14.0/lib"
