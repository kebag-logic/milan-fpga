#!/bin/sh
# Actual gPTP processor PR61/PR62 against both recorded targets, plus the
# decision's four raw patch hashes.  Usage: actual_pr62.sh <scripts-dir> <gptp-clone>
scripts=${1:?scripts}; repo=${2:?clone}
cd "$repo" || exit 9
for target in f0f1c055ee5226f08e656c27cb1bf4c355be11ae c1b617435824929a790739ea8585c3fe1a328cc0; do
  for head in 9790ac736e6d10301ad814ffdf73dbe37b59768b 3db86812096830fada2f5f276fa5f4d9f37d1d14; do
    out=$(PYTHONDONTWRITEBYTECODE=1 python3 "$scripts/check_merge_containment.py" --no-fetch --base "$target" "$head" 2>&1)
    echo "target=$target head=$head rc=$?"
    echo "$out" | sed 's/^/    /'
  done
done
for pair in 3db86812096830fada2f5f276fa5f4d9f37d1d14 5602e70bb4cf70c2e0e39e846e26925e27659e32 \
            9790ac736e6d10301ad814ffdf73dbe37b59768b 20927af74752620b2ad0f973e8be3203994b5547; do
  parent=$(git rev-parse "$pair^")
  h=$(git diff --no-ext-diff --no-textconv --no-renames "$parent" "$pair" | sha256sum | cut -d' ' -f1)
  echo "patch-sha256 $pair $h"
done
