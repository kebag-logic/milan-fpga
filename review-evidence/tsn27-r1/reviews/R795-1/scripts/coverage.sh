#!/bin/bash
# Informative: coverage gate at the exact head with this host's gcc (CI's compiler differs).
set -u; . "$(dirname "$0")/env.sh"
O=$RCP/coverage-host; B=$SCR/build-coverage; mkdir -p "$O"; rm -rf "$B"
gcc --version | head -1 > "$O/compiler.txt"
cmake -S "$REPO" -B "$B" -DCMAKE_BUILD_TYPE=Debug -DTSN_COVERAGE=ON > "$O/configure.log" 2>&1; echo "configure $?" > "$O/rc.txt"
cmake --build "$B" -j4 > "$O/build.log" 2>&1; echo "build $?" >> "$O/rc.txt"
find "$B" -name '*.gcda' -delete
ctest --test-dir "$B" -j4 > "$O/ctest.log" 2>&1; echo "ctest $?" >> "$O/rc.txt"
(cd "$REPO" && python3 scripts/coverage.py "$B") > "$O/coverage.log" 2>&1; echo "coverage $?" >> "$O/rc.txt"
cat "$O/rc.txt"; head -6 "$O/coverage.log"
