#!/bin/sh
# Usage: plant_at_rev.sh <clone> <rev> <empty dir> <plant name> <plant catalogue rev>
# Exports <rev>, applies the named plant from tests/mutations.json at <plant catalogue rev> (its old text must
# occur exactly once in <rev>), builds acmp_tests and runs the whole ACMP binary. rc 0 means the plant escapes.
set -u
C=$1; R=$2; T=$3; M=$4; K=$5; HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/env.sh"
mkdir -p "$T"; (cd "$C" && git archive "$R") | tar -x -C "$T"
(cd "$C" && git show "$K:tests/mutations.json") > "$T/catalogue.json"
python3 -I - "$T" "$M" <<'PY' || exit 3
import json, sys, pathlib
root = pathlib.Path(sys.argv[1]); m = [x for x in json.load(open(root / 'catalogue.json')) if x['name'] == sys.argv[2]][0]
f = root / m['path']; s = f.read_text(); assert s.count(m['old']) == 1, 'old text not unique'; f.write_text(s.replace(m['old'], m['new']))
PY
cmake -S "$T" -B "$T/build" -DCMAKE_BUILD_TYPE=Debug -G Ninja >/dev/null && cmake --build "$T/build" --target acmp_tests -j3 >/dev/null || exit 2
"$T/build/acmp_tests" > "$T/run.log" 2>&1; rc=$?
echo "rev $R plant $M rc $rc $(grep -E '^\[  (PASSED|FAILED)  \]' "$T/run.log" | tr '\n' ' ')"
