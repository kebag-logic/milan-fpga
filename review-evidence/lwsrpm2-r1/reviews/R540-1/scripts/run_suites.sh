#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Build and run ctest, the unit runner and behave for both Registrar profiles concurrently.
# Usage: run_suites.sh <source-tree> <work-dir> <cgreen-prefix> <receipt-dir>
set -u
SRC=$1; WORK=$2; PREFIX=$3; OUT=$4
mkdir -p "$WORK" "$OUT"
export CMAKE_PREFIX_PATH="$PREFIX" LD_LIBRARY_PATH="$PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
profile() {
    name=$1; flag=$2; b="$WORK/build-$name"
    step() { label=$1; shift; "$@" > "$OUT/$name-$label.log" 2>&1; echo $? > "$OUT/$name-$label.rc"; }
    step configure cmake -S "$SRC" -B "$b" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=$flag
    step build cmake --build "$b" --parallel 8
    step ctest ctest --test-dir "$b" --output-on-failure
    step unit "$b/unit_tests"
    (cd "$SRC" && SHLAN_LIBRARY="$b/libshlan.so" behave --no-color) > "$OUT/$name-behave.log" 2>&1; echo $? > "$OUT/$name-behave.rc"
}
profile ieee OFF &
profile milan ON &
wait
for f in "$OUT"/*.rc; do printf '%s %s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done
