#!/bin/bash
# Build one (point, arm) as the formal measurement's legs do (build.build: CPU regions cover, the split L1, no XIP),
# then run the named groups with run.py --reuse-build and the formal options; print each group log's sha256.
# usage: confirm_group.sh <clone> <build dir> <point> <arm> <groups>
set -u
c=$1; b=$2; pt=$3; arm=$4; groups=$5
h=$c/tb/verilator/ctrl_service_budget
python3 -B - "$h" "$b" "$pt" "$arm" <<'PY' || exit 3
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1]); sys.dont_write_bytecode = True
import build as builder, run
shape, n_if = run.POINTS[sys.argv[3]]
builder.build(Path(sys.argv[2]).resolve(), shape, n_if, mutation='none', variant=sys.argv[4],
              core=builder.Core('cover', 'split', False))
print('BUILT')
PY
python3 -B "$h/run.py" --point "$pt" --build-dir "$b" --reuse-build --out "$b/part0" --groups "$groups" \
  --record-budget-findings --record-share-findings --jobs 2 --variant "$arm"
rc=$?
for g in ${groups//,/ }; do echo "LOG $g $(sha256sum "$b/part0/$g.log" | cut -c1-64)"; done
exit $rc
