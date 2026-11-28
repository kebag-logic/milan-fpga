#!/bin/sh
# Reviewer environment: pinned GoogleTest 1.14.0 and Clang 18 lexer; host GCC and Clang for builds.
# TOOLS is the directory holding gtest-1.14.0, clang-18 and clang-tidy-18 installs.
: "${TOOLS:?set TOOLS to the pinned tool directory}"
export PKG_CONFIG_PATH="$TOOLS/gtest-1.14.0/lib/pkgconfig"
export CMAKE_PREFIX_PATH="$TOOLS/gtest-1.14.0"
export TSN_CLANG="$TOOLS/clang-18/bin/clang-18"
export PATH="$TOOLS/clang-18/bin:$PATH"
unset CPATH CPLUS_INCLUDE_PATH C_INCLUDE_PATH LIBRARY_PATH
