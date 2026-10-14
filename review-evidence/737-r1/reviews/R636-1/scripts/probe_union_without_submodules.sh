#!/bin/bash
# Reproduce the hosted union-job checkout (actions/checkout@v4 defaults: no
# submodules) and run the production inventory derivation for each split suite.
# Usage: probe_union_without_submodules.sh <source-clone> <commit> <scratch-dir>
set -u
src=$1; commit=$2; dir=$3
rm -rf "$dir"; git clone -q --no-recurse-submodules "$src" "$dir" && git -C "$dir" checkout -q "$commit" || exit 9
cd "$dir"
echo "head $(git rev-parse HEAD); submodules initialised: $(git submodule status | grep -vc '^-')"
env -i PATH=/usr/bin:/bin HOME="$dir" PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import sys
sys.path.insert(0, "scripts")
from ci_suite_pieces import inventory, PIECE_SECONDS
bad = 0
for s in PIECE_SECONDS:
    try:
        print(s, "inventory OK:", len(inventory(s)), "cases")
    except Exception as e:
        bad += 1
        print(s, "inventory REFUSED:", type(e).__name__)
print("suites whose union job and collector cannot derive an inventory:", bad)
PY
