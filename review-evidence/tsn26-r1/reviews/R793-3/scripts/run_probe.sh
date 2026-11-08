#!/bin/sh
# Usage: run_probe.sh <clone> <empty probe dir> <revision> <probe.cpp> <gtest filter>
# Exports the revision, inserts the probe at the end of the anonymous test namespace in tests/test_acmp.cpp
# (before main's Wire test), builds acmp_tests and runs the filter. Never touches the clone.
set -eu
C=$1; T=$2; REV=$3; PROBE=$4; FILTER=$5; HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/env.sh"
mkdir -p "$T"; (cd "$C" && git archive "$REV") | tar -x -C "$T"
python3 -I - "$T/tests/test_acmp.cpp" "$PROBE" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
s = s.replace('#include <cstring>', '#include <algorithm>\n#include <cstdio>\n#include <cstring>', 1)
anchor = '\n}\n\n// REQ: ACMP-02\nTEST(Wire,'
assert s.count(anchor) == 1
p.write_text(s.replace(anchor, '\n' + pathlib.Path(sys.argv[2]).read_text() + anchor, 1))
PY
cmake -S "$T" -B "$T/build" -DCMAKE_BUILD_TYPE=Debug -G Ninja >/dev/null
cmake --build "$T/build" --target acmp_tests -j8 >/dev/null
"$T/build/acmp_tests" --gtest_filter="$FILTER"
