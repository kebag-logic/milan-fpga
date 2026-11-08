#!/bin/sh
# Usage: run_probe_timer_ahead.sh <clone> <empty probe dir> [revision, default HEAD]
# Exports the revision, inserts probe_timer_ahead.cpp at the end of the anonymous test namespace in
# tests/test_acmp.cpp (before the Wire test), builds acmp_tests and runs the probe. Never touches the clone.
set -eu
C=$1; T=$2; REV=${3:-HEAD}; HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/env.sh"
mkdir -p "$T"; (cd "$C" && git archive "$REV") | tar -x -C "$T"
python3 -I - "$T/tests/test_acmp.cpp" "$HERE/probe_timer_ahead.cpp" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text()
s = s.replace('#include <cstring>', '#include <cstdio>\n#include <cstring>', 1)
anchor = '\n}\n\n// REQ: ACMP-02\nTEST(Wire,'
add = pathlib.Path(sys.argv[2]).read_text()
if s.count(anchor) == 1:
    p.write_text(s.replace(anchor, '\n' + add + anchor, 1))
else:
    # Before main's Wire test was merged, the anonymous namespace closes the file.
    i = s.rstrip().rfind('}')
    p.write_text(s[:i] + add + '\n}\n')
PY
cmake -S "$T" -B "$T/build" -DCMAKE_BUILD_TYPE=Debug -G Ninja >/dev/null
cmake --build "$T/build" --target acmp_tests -j4 >/dev/null
"$T/build/acmp_tests" --gtest_filter='AcmpOwedProbe.*'
