# Pinned toolchain for the tsn-c-stack gates: set TOOLS to the directory holding
# gtest-1.14.0, clang-18 and clang-tidy-18 before sourcing this file.
: "${TOOLS:?set TOOLS to the pinned toolchain directory}"
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig
export CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0
export LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
export PATH=$TOOLS/clang-tidy-18/bin:$TOOLS/clang-18/bin:$PATH
