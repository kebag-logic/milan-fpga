#!/bin/sh
# Disable resmap_map.py's stray-owner census check in a disposable copy and run its self-test.
# Usage: probe_stray_owner.sh <copy of syn/resmap/resmap_map.py>
# A self-test rc of 0 means no arm exercises that check. The copy is restored afterwards.
set -eu
f="$1"
cp "$f" "$f.orig"
python3 - "$f" <<'PY'
import sys
p = sys.argv[1]; t = open(p).read(); old = '    if stray:\n        failures.append'
assert t.count(old) == 1
open(p, 'w').write(t.replace(old, '    if False:\n        failures.append'))
PY
rc=0; python3 "$f" --selftest || rc=$?
echo "stray-owner check disabled: selftest rc=$rc"
mv "$f.orig" "$f"
