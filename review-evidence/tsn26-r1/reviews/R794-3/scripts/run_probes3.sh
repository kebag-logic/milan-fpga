#!/bin/bash
# SPDX-License-Identifier: MIT
# usage: run_probes3.sh HEAD_TREE WORK OUT INC FILTER [PLANT PLANTS_JSON]
# Copies HEAD_TREE, appends INC inside the anonymous namespace of tests/test_acmp.cpp, optionally applies
# one plant (scripts/apply_plant.py), builds acmp_tests and runs the tests matching FILTER.
# Needs TOOLS set to a prefix holding gtest-1.14.0. HEAD_TREE is never modified.
set -eu
src=$1; work=$2; out=$3; inc=$4; filter=$5; plant=${6:-}; plants=${7:-}; here=$(cd "$(dirname "$0")" && pwd)
: "${TOOLS:?set TOOLS}"
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
rm -rf "$work"; mkdir -p "$work"; cp -a "$src" "$work/tree"
python3 -I - "$work/tree" "$inc" <<'PY'
import sys, pathlib
tree, inc = pathlib.Path(sys.argv[1]), sys.argv[2]
t = tree / 'tests/test_acmp.cpp'
text = t.read_text()
marker = '\n}\n\n// REQ: ACMP-02\nTEST(Wire, W1PutBeWritesTheLowBytesMostSignificantFirst)'
assert text.count(marker) == 1, 'anonymous namespace end not found'
at = text.index(marker) + 1
t.write_text('#include <cstdio>\n' + text[:at] + open(inc).read() + '\n' + text[at:])
PY
if [ -n "$plant" ]; then python3 -I "$here/apply_plant.py" "$work/tree" "$plant" "$plants" > "$out"; else : > "$out"; fi
cmake -S "$work/tree" -B "$work/build" -DCMAKE_BUILD_TYPE=Debug > "$work/configure.log" 2>&1
cmake --build "$work/build" --target acmp_tests -j4 > "$work/build.log" 2>&1
set +e
"$work/build/acmp_tests" --gtest_filter="$filter" >> "$out" 2>&1
echo "rc $?" >> "$out"
