#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Regenerate the coverage ratchet in a disposable copy of the exact head and diff it
# against the committed file. Host gcc, so this corroborates and does not replace CI.
set -u
. "$(dirname "$0")/env.sh"
w=$SCRATCH/ratchet; rm -rf "$w"; mkdir -p "$w/tree"
git -C "$CLONE" archive c687810b74b53b69c1fbdff7bfd0ec9da94eaa78 | tar -x -C "$w/tree"
cmake -S "$w/tree" -B "$w/build" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ -DTSN_COVERAGE=ON > "$w/configure.log" 2>&1 || exit 1
cmake --build "$w/build" -j3 > "$w/build.log" 2>&1 || exit 1
ctest --test-dir "$w/build" -j3 > "$w/test.log" 2>&1 || { tail "$w/test.log"; exit 1; }
gcc --version | head -1
(cd "$w/tree" && PYTHONDONTWRITEBYTECODE=1 python3 scripts/coverage.py "$w/build"); echo "coverage check rc=$?"
(cd "$w/tree" && PYTHONDONTWRITEBYTECODE=1 python3 scripts/coverage.py "$w/build" --write >/dev/null); echo "coverage write rc=$?"
git -C "$CLONE" show c687810b74b53b69c1fbdff7bfd0ec9da94eaa78:tests/coverage.ratchet | diff - "$w/tree/tests/coverage.ratchet" && echo "regenerated ratchet identical to committed"
