# SPDX-License-Identifier: MIT
# Source before running the tsn-c-stack gates: the gates require GoogleTest 1.14.0 and Clang 18.
T=${TSN_TOOLS:?set TSN_TOOLS to the root of the pinned Clang 18 and GoogleTest 1.14.0 tools}
export PATH=$T/clang-18/bin:$T/clang-tidy-18/bin:$PATH
export PKG_CONFIG_PATH=$T/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$T/gtest-1.14.0 LD_LIBRARY_PATH=$T/gtest-1.14.0/lib
