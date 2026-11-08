# Pinned toolchain environment used by every reviewer campaign (portable: override TOOLS).
: "${TOOLS:?set TOOLS to the pinned toolchain prefix holding gtest-1.14.0, clang-18 and clang-tidy-18}"
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
export PATH=$TOOLS/clang-tidy-18/bin:$TOOLS/clang-18/bin:$PATH
