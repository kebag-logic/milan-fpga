# Pinned toolchain locations are taken from TOOLS (GoogleTest 1.14.0, Clang 18.1.3).
: "${TOOLS:?set TOOLS to the pinned toolchain directory}"
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
export PATH=$TOOLS/clang-tidy-18/bin:$TOOLS/clang-18/bin:$PATH
