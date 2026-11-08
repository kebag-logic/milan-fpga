#!/bin/sh
# SPDX-License-Identifier: MIT
# usage: run_gates.sh CLONE WORK   (environment from clang18_shims.sh and the gtest variables)
# Runs the gate kit (without --graphs: no Mermaid CLI on the host) and the RV32 gate, each with its log
# and rc file, then the sanitizer arm again with the host clang (the pinned clang 18 cannot parse the
# host's libstdc++ 16 headers).
set -u
c=$1; w=$2; mkdir -p "$w"
(cd "$c" && python3 scripts/validate.py --work "$w/val" --jobs 8 > "$w/val.log" 2>&1; echo $? > "$w/val.rc") &
(cd "$c" && python3 scripts/baremetal.py --work "$w/rv32" --jobs 4 > "$w/rv32.log" 2>&1; echo $? > "$w/rv32.rc") &
wait
b=$w/san23; mkdir -p "$b/temp"
cmake -S "$c" -B "$b/build" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=/usr/bin/clang -DCMAKE_CXX_COMPILER=/usr/bin/clang++ -DTSN_SANITIZERS=ON > "$b/configure.log" 2>&1
cmake --build "$b/build" -j8 > "$b/build.log" 2>&1
TMPDIR=$b/temp ASAN_OPTIONS=detect_leaks=1:halt_on_error=1 UBSAN_OPTIONS=halt_on_error=1 ctest --test-dir "$b/build" --output-on-failure -j8 > "$b/test.log" 2>&1; echo $? > "$b/test.rc"
