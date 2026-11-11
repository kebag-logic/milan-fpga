#!/bin/bash
# The validate.py clang-sanitizers gate with a given clang (the pinned 18 cannot use this host's libstdc++).
# usage: sanitizer_gate.sh SRC OUT CC CXX
set -u
SRC=$1 O=$2 CC=$3 CXX=$4
D=$(cd "$(dirname "$0")" && pwd); S=$D/../scratch; . "$D/env.sh"
export ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 UBSAN_OPTIONS=halt_on_error=1
rm -rf "$O"; mkdir -p "$O"
cmake -S "$SRC" -B "$O/b" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DTSN_SANITIZERS=ON > "$O/configure.log" 2>&1; echo $? > "$O/configure.rc"
cmake --build "$O/b" -j16 > "$O/build.log" 2>&1; echo $? > "$O/build.rc"
ctest --test-dir "$O/b" --output-on-failure -j16 > "$O/test.log" 2>&1; echo $? > "$O/test.rc"
