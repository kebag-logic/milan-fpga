#!/bin/bash
# One candidate wire.h substitution in a scratch copy without the W1 test: build and run every hosted test.
# usage: candidate.sh REPO WORK TAG OLD NEW   (OLD/NEW are Python string literals)
set -u
. $HOME/milan-fpga-management/2026-09-23/tsn27-a751/scripts/env.sh
REPO=$1 W=$2 TAG=$3 OLD=$4 NEW=$5
D=$W/$TAG; rm -rf "$D"; mkdir -p "$D"
(cd "$REPO" && git ls-files -co --exclude-standard | grep -v '^build' | tar -cf - -T -) | tar -xf - -C "$D"
python3 -I - "$D" "$OLD" "$NEW" <<'PY'
import ast, sys
from pathlib import Path
d = Path(sys.argv[1]); old = ast.literal_eval(sys.argv[2]); new = ast.literal_eval(sys.argv[3])
p = d / 'include/wire.h'; t = p.read_text(); assert t.count(old) == 1, old
p.write_text(t.replace(old, new))
p = d / 'tests/test_acmp.cpp'; s = p.read_text()
start = s.index('// REQ: ACMP-02\nTEST(Wire, W1PutBeWritesTheLowBytesMostSignificantFirst)')
end = s.index('\n}\n', start) + 3
p.write_text(s[:start] + s[end:])
PY
cmake -S "$D" -B "$D/build" -DCMAKE_BUILD_TYPE=Debug > "$D/cfg.log" 2>&1 && cmake --build "$D/build" -j8 > "$D/build.log" 2>&1
b=$?
ctest --test-dir "$D/build" -j8 > "$D/ctest.log" 2>&1; c=$?
echo "$TAG build=$b ctest=$c $(grep -E 'tests passed' "$D/ctest.log")"
