# Environment for the tsn-c-stack gates on a host whose default GoogleTest and Clang are newer than the pins.
# Usage: TOOLS=<directory holding clang-18/, clang-tidy-18/ and gtest-1.14.0/> . env.sh
# Puts the Clang 18.1.3 lexer, clang-tidy and GoogleTest/GMock 1.14.0 ahead of the host's versions.
: "${TOOLS:?set TOOLS to the pinned toolchain directory}"
export PATH=$TOOLS/clang-18/bin:$TOOLS/clang-tidy-18/bin:$PATH
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig
export CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0
export LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
