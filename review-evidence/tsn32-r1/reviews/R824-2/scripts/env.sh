# Pinned toolchain for the stack's gates. Set TOOLS to the directory holding gtest-1.14.0, clang-18 and clang-tidy-18;
# S is the packet's scratch directory, whose bin/ holds clang and clang++ links to clang-18.
: "${TOOLS:?set TOOLS to the pinned toolchain directory}"
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
export PATH=$S/bin:$TOOLS/clang-tidy-18/bin:$PATH
