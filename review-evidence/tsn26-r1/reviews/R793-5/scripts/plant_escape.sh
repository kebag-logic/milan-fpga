#!/bin/sh
# Usage: plant_escape.sh <clone> <empty dir> <revision> <plant name> <test to exclude>
# Exports the revision, applies the registered plant <plant name> from its tests/mutations.json (old -> new, which
# must occur exactly once), builds acmp_tests and runs (1) the whole ACMP binary and (2) the binary without the named
# test. Prints the failing tests of each run. A plant whose run (2) passes escapes without that test.
set -u
C=$1; T=$2; REV=$3; NAME=$4; EXCL=$5; HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/env.sh"
mkdir -p "$T"; (cd "$C" && git archive "$REV") | tar -x -C "$T"
python3 -I - "$T" "$NAME" <<'PY' || exit 2
import json, sys, pathlib
root = pathlib.Path(sys.argv[1]); name = sys.argv[2]
m = [x for x in json.load(open(root / 'tests/mutations.json')) if x['name'] == name]
assert len(m) == 1, name
m = m[0]; p = root / m['path']; s = p.read_text()
assert s.count(m['old']) == 1, 'old text not unique'
p.write_text(s.replace(m['old'], m['new'], 1))
print('applied', name, 'to', m['path'])
PY
cmake -S "$T" -B "$T/build" -DCMAKE_BUILD_TYPE=Debug -G Ninja >/dev/null && cmake --build "$T/build" --target acmp_tests -j4 >/dev/null || exit 3
"$T/build/acmp_tests" > "$T/full.log" 2>&1; echo "full suite rc=$?"; grep -a '^\[  FAILED  \] [A-Za-z]' "$T/full.log" | sort -u; grep -a '^\[==========\] .* ran' "$T/full.log"
"$T/build/acmp_tests" --gtest_filter="-$EXCL" > "$T/excl.log" 2>&1; echo "without $EXCL rc=$?"; grep -a '^\[  FAILED  \] [A-Za-z]' "$T/excl.log" | sort -u; grep -a '^\[==========\] .* ran' "$T/excl.log"
