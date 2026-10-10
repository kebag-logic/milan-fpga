#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Usage: gate.sh <source-tree> <milan OFF|ON> <build-dir> <log-prefix> <cgreen-prefix>
# Configure, build, run ctest and the unit runner, then behave, recording each exit code.
set -u
src=$1; milan=$2; build=$3; log=$4; prefix=$5
export LD_LIBRARY_PATH="$prefix/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
step() { name=$1; shift; "$@" > "$log.$name.log" 2>&1; rc=$?; echo "$name rc=$rc" | tee -a "$log.rc"; return $rc; }
: > "$log.rc"
step configure cmake -S "$src" -B "$build" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN="$milan" -DCMAKE_PREFIX_PATH="$prefix" || exit 1
step build cmake --build "$build" --parallel 4 || exit 1
step ctest ctest --test-dir "$build" --output-on-failure || true
runner="$build/unit_tests"
step unit "$runner" || true
(cd "$src" && SHLAN_LIBRARY="$build/libshlan.so" step behave python3 -m behave --no-color) || true
