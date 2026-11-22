# Pinned toolchain for the tsn-c-stack gates (sourced). TOOLS names the pinned tool directory.
T=${TOOLS:?set TOOLS to the directory holding gtest-1.14.0, clang-18 and clang-tidy-18}
export PKG_CONFIG_PATH=$T/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$T/gtest-1.14.0 LD_LIBRARY_PATH=$T/gtest-1.14.0/lib
export PATH=$T/clang-18/bin:$T/clang-tidy-18/bin:$PATH
export PYTHONDONTWRITEBYTECODE=1
