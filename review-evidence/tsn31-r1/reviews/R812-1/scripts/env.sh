# Pinned tsn-c-stack gate toolchain: Clang 18.1.3 (+ matching compiler-rt 18.1.3 in scratch), clang-tidy 18.1.3,
# GoogleTest/GMock 1.14.0, Mermaid CLI 11.16.0 from the user's PATH. Usage: . env.sh <packet>
P=${1:?packet}; TSN_TOOLS=${TOOLS:?set TOOLS to the pinned toolchain root}
export PATH=$P/scratch/bin:$TSN_TOOLS/clang-tidy-18/bin:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin
export PKG_CONFIG_PATH=$TSN_TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$TSN_TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$TSN_TOOLS/gtest-1.14.0/lib
export TSN_CLANG=$P/scratch/bin/clang-18
