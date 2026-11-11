#!/bin/sh
# The validate.py clang-sanitizers configuration (configure, build, ctest) with the host Clang standing in for
# the pinned Clang 18.1.3, whose C++ front end cannot parse the host's libstdc++ 16 headers.
# Same options and runtime settings as scripts/validate.py.
# Usage: TSN_TOOLS=<tools> sanitizers_standin.sh TREE WORK JOBS
set -eu
: "${TSN_TOOLS:?set TSN_TOOLS to the pinned tool root}"
tree=$1; work=$2; jobs=$3
mkdir -p "$work/temp"
export TMPDIR="$work/temp" ASAN_OPTIONS='detect_leaks=1:halt_on_error=1' UBSAN_OPTIONS='halt_on_error=1'
export PKG_CONFIG_PATH="$TSN_TOOLS/gtest-1.14.0/lib/pkgconfig" CMAKE_PREFIX_PATH="$TSN_TOOLS/gtest-1.14.0" LD_LIBRARY_PATH="$TSN_TOOLS/gtest-1.14.0/lib"
clang --version | head -1
cmake -S "$tree" -B "$work/clang-sanitizers" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DTSN_SANITIZERS=ON
cmake --build "$work/clang-sanitizers" -j"$jobs"
ctest --test-dir "$work/clang-sanitizers" --output-on-failure -j"$jobs"
