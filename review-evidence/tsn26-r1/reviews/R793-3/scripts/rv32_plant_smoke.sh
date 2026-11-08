#!/bin/sh
# Usage: rv32_plant_smoke.sh <clone at head> <empty dir> <plant name from tests/mutations.json>
# Applies one plant to an exported copy and runs the bare-metal gate there; a nonzero rc means the
# RV32 smoke check caught the plant.
set -u
C=$1; T=$2; M=$3
mkdir -p "$T"; (cd "$C" && git archive HEAD) | tar -x -C "$T"
python3 -I - "$T" "$M" <<'PY'
import json, sys, pathlib
root = pathlib.Path(sys.argv[1]); m = [x for x in json.load(open(root / 'tests/mutations.json')) if x['name'] == sys.argv[2]][0]
f = root / m['path']; s = f.read_text(); assert s.count(m['old']) == 1; f.write_text(s.replace(m['old'], m['new']))
PY
cd "$T" && python3 scripts/baremetal.py --work "$T/build-rv32" --jobs 4; echo "rc $?"
