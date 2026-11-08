#!/bin/bash
# Plant one registered defect in a scratch copy, with and without the W1 test, then build and run every hosted test.
# usage: escape.sh REPO WORK PLANT_NAME
set -u
. $HOME/milan-fpga-management/2026-09-23/tsn27-a751/scripts/env.sh
REPO=$1 W=$2 NAME=$3
for variant in with-w1 without-w1; do
  D=$W/$NAME/$variant
  rm -rf "$D"; mkdir -p "$D"
  (cd "$REPO" && git ls-files -co --exclude-standard | grep -v '^build' | tar -cf - -T -) | tar -xf - -C "$D"
  python3 -I - "$D" "$NAME" "$variant" <<'PY'
import json, re, sys
from pathlib import Path
d, name, variant = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
m = next(m for m in json.loads((d / 'tests/mutations.json').read_text()) if m['name'] == name)
t = (d / m['path']).read_text()
assert t.count(m['old']) == 1
(d / m['path']).write_text(t.replace(m['old'], m['new']))
if variant == 'without-w1':
    p = d / 'tests/test_acmp.cpp'
    s = p.read_text()
    start = s.index('// REQ: ACMP-02\nTEST(Wire, W1PutBeWritesTheLowBytesMostSignificantFirst)')
    end = s.index('\n}\n', start) + 3
    s = s[:start] + s[end:]
    assert 'W1PutBe' not in s
    p.write_text(s)
PY
  cmake -S "$D" -B "$D/build" -DCMAKE_BUILD_TYPE=Debug > "$D/cfg.log" 2>&1; echo "cfg=$?" > "$D/rc.txt"
  cmake --build "$D/build" -j16 > "$D/build.log" 2>&1; echo "build=$?" >> "$D/rc.txt"
  ctest --test-dir "$D/build" --output-on-failure -j16 > "$D/ctest.log" 2>&1; echo "ctest=$?" >> "$D/rc.txt"
  for b in "$D"/build/test_* "$D"/build/*_tests "$D"/build/tsn_*; do [ -x "$b" ] && [ -f "$b" ] && "$b" --gtest_brief=1 > "$D/$(basename "$b").gtest.log" 2>&1; done
  echo "== $NAME $variant: $(tr '\n' ' ' < "$D/rc.txt")"; grep -E "tests passed|FAILED|Failed" "$D/ctest.log" | head -12
done
