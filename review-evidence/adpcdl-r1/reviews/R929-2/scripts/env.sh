# Pinned GoogleTest 1.14.0 and Clang 18: set TSN_TOOLS to the directory that holds gtest-1.14.0 and clang-18.
: "${TSN_TOOLS:?set TSN_TOOLS}"
export PKG_CONFIG_PATH=$TSN_TOOLS/gtest-1.14.0/lib/pkgconfig
export CMAKE_PREFIX_PATH=$TSN_TOOLS/gtest-1.14.0
export LD_LIBRARY_PATH=$TSN_TOOLS/gtest-1.14.0/lib
export PATH=$TSN_TOOLS/clang-18/bin:$PATH
