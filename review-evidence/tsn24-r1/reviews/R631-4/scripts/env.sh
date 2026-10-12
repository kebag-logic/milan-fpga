#!/usr/bin/env bash
# Source this file after setting optional dependency prefixes.
: "${TSN_GTEST_PREFIX:?Set the GoogleTest 1.14.0 installation prefix}"
: "${TSN_CLANG_PREFIX:?Set the extracted Clang 18 installation prefix}"
export PATH="$TSN_CLANG_PREFIX/bin:$PATH"
export PKG_CONFIG_PATH="$TSN_GTEST_PREFIX/lib/pkgconfig"
export CMAKE_PREFIX_PATH="$TSN_GTEST_PREFIX"
export LD_LIBRARY_PATH="$TSN_GTEST_PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
unset CPATH CPLUS_INCLUDE_PATH C_INCLUDE_PATH LIBRARY_PATH
export TSN_CLANG="$TSN_CLANG_PREFIX/root/usr/bin/clang-18"
export LD_LIBRARY_PATH="$TSN_CLANG_PREFIX/root/usr/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"
