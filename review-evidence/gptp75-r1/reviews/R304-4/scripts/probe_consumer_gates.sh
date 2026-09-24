#!/bin/sh
# Run the parent's C++ and Python idiom gates with gptp-processor committed
# (locally, never pushed) at each given FPGA-gPTP revision.
# Usage: probe_consumer_gates.sh <parent-clone-at-573f0052> <rev>...
set -u
P=$1; shift
cd "$P" || exit 2
BASE=$(git rev-parse HEAD)
for rev in "$@"; do
  git reset -q --hard "$BASE"
  git -C gptp-processor checkout -q --detach "$rev" || exit 2
  git add gptp-processor
  git -c user.name=reviewer -c user.email=reviewer@invalid commit -q -m "probe: gitlink $rev" || true
  echo "=== parent $BASE + gptp-processor $(git ls-tree HEAD gptp-processor | awk '{print $3}') (commit $(git rev-parse --short HEAD))"
  for g in check_cpp_idiom check_py_idiom; do
    out=$(python3 scripts/$g.py 2>&1); rc=$?
    echo "--- $g rc=$rc"
    printf '%s\n' "$out" | grep -E 'FAIL|long function|unannotated|undocumented|ratchet|REFUSED|OK|PASS|pass' | head -30
  done
done
git reset -q --hard "$BASE"
git -C gptp-processor checkout -q --detach "$(git ls-tree HEAD gptp-processor | awk '{print $3}')"
