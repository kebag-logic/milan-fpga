#!/usr/bin/env bash
# [R293] R293-3: run the containment checker on the composed history, read-only
# with respect to the review clone (a disposable local clone is used).
# Usage: smoke_containment.sh <review-clone> <python> <scratch-dir>
set -u
SRC=b0347a4fd668f8d40bdf40a142ac0ea70167acd1
CAND=177867daf3b35ba41b8c51f8c35c8509643dda22
d="$3/smoke"; rm -rf "$d"
git clone -q --no-checkout "$1" "$d" && cd "$d" || exit 2
git -c advice.detachedHead=false checkout -q "$CAND" || exit 2
echo "clone HEAD $(git rev-parse HEAD)"
for mode in "" "--current-retention"; do
  echo "=== mode:${mode:-default}"
  "$2" scripts/check_merge_containment.py $mode --no-fetch --base "$CAND" "$SRC"
  echo "rc=$?"
done 2>&1
