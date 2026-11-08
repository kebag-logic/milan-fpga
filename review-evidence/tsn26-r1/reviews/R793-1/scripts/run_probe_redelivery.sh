#!/bin/sh
# Usage: run_probe_redelivery.sh <clone at head> <empty probe dir>
# Exports the head tree, appends probe_redelivery.cpp inside the test namespace of tests/test_acmp.cpp,
# builds acmp_tests and runs the AcmpOwed and A19 tests. Never touches the clone's tracked files.
set -eu
C=$1; T=$2; HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/env.sh"
mkdir -p "$T"; (cd "$C" && git archive HEAD) | tar -x -C "$T"
python3 -I - "$T/tests/test_acmp.cpp" "$HERE/probe_redelivery.cpp" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); s = p.read_text().replace('#include <cstring>', '#include <cstdio>\n#include <cstring>', 1)
add = pathlib.Path(sys.argv[2]).read_text(); i = s.rstrip().rfind('}')
p.write_text(s[:i] + add + '\n}\n')
PY
cmake -S "$T" -B "$T/build" -DCMAKE_BUILD_TYPE=Debug -G Ninja >/dev/null
cmake --build "$T/build" --target acmp_tests -j8 >/dev/null
"$T/build/acmp_tests" --gtest_filter='AcmpOwed.*:AcmpCore.A19*'
