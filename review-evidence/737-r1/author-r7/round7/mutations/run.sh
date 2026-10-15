#!/bin/bash
# usage: run.sh <label> <file> <old> <new>; apply one mutation in the clone, run the self-test, restore.
set -u
M=$VALIDATION_STORAGE/737-a614/r7/mut; cd $M/clone
label=$1; file=$2; old=$3; new=$4
cp "$file" "$M/$label.orig"
$VALIDATION_STORAGE/737-a614/venv/bin/python3 - "$file" "$old" "$new" <<'PY'
import sys; from pathlib import Path
p = Path(sys.argv[1]); s = p.read_text(); assert s.count(sys.argv[2]) == 1, "anchor"; p.write_text(s.replace(sys.argv[2], sys.argv[3]))
PY
$VALIDATION_STORAGE/737-a614/venv/bin/python3 scripts/ci_gate_workflows.py > "$M/$label.regen.log" 2>&1; grc=$?
$VALIDATION_STORAGE/737-a614/venv/bin/python3 scripts/ci_gate_workflows.py --check > "$M/$label.check.log" 2>&1; crc=$?
$VALIDATION_STORAGE/737-a614/venv/bin/python3 scripts/ci_gate_workflows_selftest.py > "$M/$label.log" 2>&1; rc=$?
cp "$M/$label.orig" "$file"; git checkout -q -- .github/workflows
echo "$label: regenerate rc=$grc, generator --check rc=$crc selftest rc=$rc; $(grep -m1 -E 'Error|assert' "$M/$label.log" | cut -c1-200)"
