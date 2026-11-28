#!/bin/sh
# Pinned toolchain environment for the tsn-c-stack gates on the review host.
# Source it with TOOLS set to the directory holding gtest-1.14.0, clang-18 and clang-tidy-18.
TOOLS=${TOOLS:?set TOOLS to the pinned toolchain directory}
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig
export CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0
export LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
export PATH=$TOOLS/clang-tidy-18/bin:$TOOLS/clang-18/bin:$PATH
