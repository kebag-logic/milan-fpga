#!/bin/sh
# Usage: run_reviewer_plants.sh <clone at head> <empty dir>
# Exports HEAD, appends reviewer_plants.json to the copy's tests/mutations.json (each with a placeholder
# killer so the driver builds it), builds every rv- plant with scripts/mutation.py --discover, then runs each
# plant's ACMP binary on the whole suite with full_suite_killers.py. rc 0 with 0 failing tests = escaped.
set -eu
C=$1; D=$2; HERE=$(cd "$(dirname "$0")" && pwd)
. "$HERE/env.sh"
mkdir -p "$D/tree"; (cd "$C" && git archive HEAD) | tar -x -C "$D/tree"
python3 -I - "$D/tree" "$HERE/reviewer_plants.json" <<'PY'
import json, sys, pathlib
root = pathlib.Path(sys.argv[1]); mine = json.load(open(sys.argv[2]))
src = (root / 'src/acmp.c').read_text()
for m in mine:
    assert src.count(m['old']) == 1, m['name']
    m['kills'] = [{"test": "AcmpOwed.HoldEndsWithTheLastHeldProbe", "needle": "is dropped with the probing it belonged to"}]
    m['original_tests'] = ["AcmpOwed.HoldEndsWithTheLastHeldProbe"]
p = root / 'tests/mutations.json'; ms = json.load(open(p)); ms.extend(mine); p.write_text(json.dumps(ms, indent=2))
PY
(cd "$D/tree" && python3 scripts/mutation.py --work "$D/work" --select rv- --jobs 8 --discover) || true
names=$(python3 -I -c "import json,sys;print(' '.join(m['name'] for m in json.load(open(sys.argv[1]))))" "$HERE/reviewer_plants.json")
python3 -I "$HERE/full_suite_killers.py" "$D/work" "$D/reviewer-plants.json" $names
