#!/bin/bash
# usage: rv32_plant.sh HEAD_TREE WORK PLANT_NAME OUT
# Applies one registered plant to a disposable copy and runs the bare-metal RV32 gate on it.
set -u
src=$1; work=$2; name=$3; out=$4
rm -rf "$work"; mkdir -p "$work"; cp -a "$src" "$work/tree"
python3 -I - "$work/tree" "$name" <<'PY'
import json, sys
from pathlib import Path
root, name = Path(sys.argv[1]), sys.argv[2]
p = {x['name']: x for x in json.loads((root / 'tests/mutations.json').read_text())}[name]
f = root / p['path']; t = f.read_text(); assert t.count(p['old']) == 1
f.write_text(t.replace(p['old'], p['new']))
PY
cd "$work/tree" && python3 scripts/baremetal.py --work "$work/rv32" --jobs 4 > "$out" 2>&1
echo "rc $?" >> "$out"
