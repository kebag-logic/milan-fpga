#!/bin/bash
# Hosted Debug build and ctest of the exact head (out-of-source), pinned GoogleTest 1.14.0.
set -u; . "$(dirname "$0")/env.sh"
O=$RCP/hosted-head; B=$SCR/build-head; mkdir -p "$O"; rm -rf "$B"
cmake -S "$REPO" -B "$B" -DCMAKE_BUILD_TYPE=Debug > "$O/configure.log" 2>&1; echo "configure $?" > "$O/rc.txt"
cmake --build "$B" -j4 > "$O/build.log" 2>&1; echo "build $?" >> "$O/rc.txt"
ctest --test-dir "$B" --output-on-failure -j4 > "$O/ctest.log" 2>&1; echo "ctest $?" >> "$O/rc.txt"
"$B/acmp_tests" --gtest_filter='Wire.*' > "$O/w1.log" 2>&1; echo "w1 $?" >> "$O/rc.txt"
cat "$O/rc.txt"; tail -3 "$O/ctest.log"
