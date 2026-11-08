#!/bin/bash
# usage: run_probes.sh HEAD_TREE WORK OUT
# Copies the exact-head tree, appends the reviewer probes to the ACMP test file, builds acmp_tests and
# runs only the probes. The reviewed tree is never modified.
set -eu
src=$1; work=$2; out=$3; here=$(cd "$(dirname "$0")" && pwd)
. "$here/env.sh"
rm -rf "$work"; mkdir -p "$work"; cp -a "$src" "$work/tree"
t="$work/tree/tests/test_acmp.cpp"
python3 -I - "$t" "$here/probe_owed.inc" <<'PY'
import sys
path, inc = sys.argv[1], sys.argv[2]
text = open(path).read()
assert text.endswith('\n}\n')
text = '#include <cstdio>\n#include <cstddef>\n' + text[:-2] + open(inc).read() + '\n}\n'
open(path, 'w').write(text)
PY
cmake -S "$work/tree" -B "$work/build" -DCMAKE_BUILD_TYPE=Debug > "$work/configure.log" 2>&1
cmake --build "$work/build" --target acmp_tests -j8 > "$work/build.log" 2>&1
set +e
"$work/build/acmp_tests" --gtest_filter='AcmpOwedProbe.*' > "$out" 2>&1
echo "rc $?" >> "$out"
