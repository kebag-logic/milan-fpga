#!/usr/bin/env bash
# #803 round 3, item 3: the six CI piece suites' case inventories (ci_suite_pieces.inventory, the owning driver's
# --list) at dev e78472ff (a clean clone) and at the lane's merge head, compared byte for byte. GNU Make 4.3 and
# CPython 3.12.3, as the hosted runner.
# usage: inventory_compare.sh
set -u
X=$VALIDATION_STORAGE/scratch/803-a693c
R=$MANAGEMENT/2026-09-23/803-a693c/receipts/shards
mkdir -p "$R" "$X/inv-err"
export PATH=$VALIDATION_STORAGE/scratch/a662/ci312/bin:$VALIDATION_STORAGE/scratch/a662/make43/bin:$PATH
{ make --version | head -1; python3 --version; } > "$R/inventory-tools.txt"
suites="milan_dp milan_dp_mclk capture_coherence maap milan_dp_render pp_shadow"
: > "$R/inventory-counts.txt"
for t in dev head; do
  if [ "$t" = dev ]; then T=$X/clone-dev-e78472ff; else T=$LANES/803-adopt-gptp; fi
  git -C "$T" rev-parse HEAD > "$R/inventory-$t-rev.txt"
  for s in $suites; do
    ( cd "$T" && python3 -I -c "
import sys, json
sys.path.insert(0, 'scripts')
from pathlib import Path
from ci_suite_pieces import inventory
print(json.dumps(inventory('$s', Path('.'))))" ) > "$R/inventory-$t-$s.json" 2> "$X/inv-err/$t-$s.err"
    rc=$?
    n=$(python3 -c "import json, sys; print(len(json.load(open(sys.argv[1]))))" "$R/inventory-$t-$s.json" 2>/dev/null)
    echo "$t $s rc=$rc cases=$n" >> "$R/inventory-counts.txt"
  done
done
: > "$R/inventory-compare.txt"
for s in $suites; do
  if cmp -s "$R/inventory-dev-$s.json" "$R/inventory-head-$s.json"; then r=identical; else r=DIFFERS; fi
  echo "$s $r" >> "$R/inventory-compare.txt"
done
cat "$R/inventory-counts.txt" "$R/inventory-compare.txt"
