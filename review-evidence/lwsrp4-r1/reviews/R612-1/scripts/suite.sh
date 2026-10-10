#!/bin/sh
# Usage: suite.sh SRC BUILD MILAN(ON|OFF) PREFIX
# Configure, build, ctest, run the unit executable and the behave scenarios.
set -u
SRC=$1; BUILD=$2; MILAN=$3; PREFIX=$4
export LD_LIBRARY_PATH="$PREFIX/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
cmake -S "$SRC" -B "$BUILD" -DCMAKE_BUILD_TYPE=Debug -DLWSRP_MILAN="$MILAN" -DCMAKE_PREFIX_PATH="$PREFIX"; echo "configure rc=$?"
cmake --build "$BUILD" --parallel 4; echo "build rc=$?"
ctest --test-dir "$BUILD" --output-on-failure; echo "ctest rc=$?"
"$BUILD/unit_tests" 2>&1 | tail -3; echo "unit rc=$?"
cd "$SRC" && SHLAN_LIBRARY="$BUILD/libshlan.so" python3 -m behave --no-color; echo "behave rc=$?"
