#!/bin/bash
# Build and run both profiles from SRC out of tree; receipts in $PKT/receipts/profiles.
set -u
. "$(dirname "$0")/env.sh"
R=$PKT/receipts/profiles; mkdir -p "$R"
run() { # name milan
  local B=$PKT/scratch/build-$1
  rm -rf "$B"
  ( cd "$SRC" &&
    cmake -S . -B "$B" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN=$2 > "$R/$1-configure.log" 2>&1; echo $? > "$R/$1-configure.rc"
    cmake --build "$B" --parallel 8 > "$R/$1-build.log" 2>&1; echo $? > "$R/$1-build.rc"
    ctest --test-dir "$B" --output-on-failure > "$R/$1-ctest.log" 2>&1; echo $? > "$R/$1-ctest.rc"
    "$B/unit_tests" > "$R/$1-unit.log" 2>&1; echo $? > "$R/$1-unit.rc"
    SHLAN_LIBRARY="$B/libshlan.so" behave > "$R/$1-behave.log" 2>&1; echo $? > "$R/$1-behave.rc" )
}
run default OFF & run milan ON & wait
for f in "$R"/*.rc; do echo "$(basename "$f") $(cat "$f")"; done
grep -h "Completed\|passed\|failed\|skipped" "$R"/*-unit.log "$R"/*-behave.log | head -20
