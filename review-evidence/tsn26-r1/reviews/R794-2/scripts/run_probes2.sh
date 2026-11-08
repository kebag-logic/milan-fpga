#!/bin/bash
# usage: run_probes2.sh HEAD_TREE WORK OUT [one-slot]
# Copies the exact-head tree, appends scripts/probe_owed2.inc to the ACMP test file, builds acmp_tests and
# runs only those probes. With "one-slot", the copy first applies the registered plant owed-bind-owes-one
# (OWED_BY_BIND 1u) as the one-slot control. The reviewed tree is never modified.
set -eu
src=$1; work=$2; out=$3; mode=${4:-}; here=$(cd "$(dirname "$0")" && pwd)
: "${TOOLS:?set TOOLS to the pinned toolchain prefix holding gtest-1.14.0}"
export PKG_CONFIG_PATH=$TOOLS/gtest-1.14.0/lib/pkgconfig CMAKE_PREFIX_PATH=$TOOLS/gtest-1.14.0 LD_LIBRARY_PATH=$TOOLS/gtest-1.14.0/lib
rm -rf "$work"; mkdir -p "$work"; cp -a "$src" "$work/tree"
python3 -I - "$work/tree" "$here/probe_owed2.inc" "$mode" <<'PY'
import sys, pathlib
tree, inc, mode = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
t = tree / 'tests/test_acmp.cpp'
text = t.read_text()
marker = '\n}\n\n// REQ: ACMP-02\nTEST(Wire, W1PutBeWritesTheLowBytesMostSignificantFirst)'
assert text.count(marker) == 1, 'anonymous namespace end not found'
at = text.index(marker) + 1
t.write_text('#include <cstdio>\n' + text[:at] + open(inc).read() + '\n' + text[at:])
if mode == 'one-slot':
    c = tree / 'src/acmp.c'
    s = c.read_text()
    assert s.count('#define OWED_BY_BIND 2u') == 1
    c.write_text(s.replace('#define OWED_BY_BIND 2u', '#define OWED_BY_BIND 1u'))
PY
cmake -S "$work/tree" -B "$work/build" -DCMAKE_BUILD_TYPE=Debug > "$work/configure.log" 2>&1
cmake --build "$work/build" --target acmp_tests -j8 > "$work/build.log" 2>&1
set +e
"$work/build/acmp_tests" --gtest_filter='AcmpOwedProbe2.*' > "$out" 2>&1
echo "rc $?" >> "$out"
