# Source to use the pinned tsn-c-stack toolchain (GoogleTest 1.14.0, Clang 18.1.3, clang-tidy 18.1.3).
# GTEST_ROOT: install prefix of GoogleTest/GMock 1.14.0.
# SHIM: a directory holding clang, clang++, clang-18, clang++-18 and clang-tidy wrappers for the pinned tools.
: "${GTEST_ROOT:?set GTEST_ROOT to the GoogleTest 1.14.0 prefix}"
: "${SHIM:?set SHIM to the pinned compiler wrapper directory}"
export PATH="$SHIM:$PATH"
export PKG_CONFIG_PATH="$GTEST_ROOT/lib/pkgconfig"
export CMAKE_PREFIX_PATH="$GTEST_ROOT"
export LD_LIBRARY_PATH="$GTEST_ROOT/lib"
