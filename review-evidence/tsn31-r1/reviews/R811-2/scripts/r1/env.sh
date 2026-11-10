# Toolchain for the review runs. Set TOOLS to the pinned root holding gtest-1.14.0, clang-18/bin (clang-18 wrapper for
# Clang 18.1.3) and clang-tidy-18/bin (clang-tidy 18.1.3); these come first on PATH, the host compilers after them.
T=${TOOLS:?set TOOLS to the pinned toolchain root}
export PATH=$T/clang-18/bin:$T/clang-tidy-18/bin:$PATH
export PKG_CONFIG_PATH=$T/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$T/gtest-1.14.0 LD_LIBRARY_PATH=$T/gtest-1.14.0/lib
