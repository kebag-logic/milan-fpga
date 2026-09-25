#!/usr/bin/env bash
# For a two-parent merge M = merge(L, D) with base B, classifies every path that
# differs from B in L, D or M: M equals L's blob (lane-only), equals D's blob
# (dev-only), or neither (both sides changed: a merge result). Also lists any
# path changed in M that neither parent changed (would be an injected edit).
set -eu
M=${1:?merge}; L=$(git rev-parse "$M^1"); D=$(git rev-parse "$M^2"); B=$(git merge-base "$L" "$D")
echo "merge=$(git rev-parse $M) lane=$L dev=$D base=$B"
blob() { git rev-parse -q --verify "$1:$2" 2>/dev/null || echo ABSENT; }
{ git diff --name-only "$B" "$L"; git diff --name-only "$B" "$D"; git diff --name-only "$B" "$M"; } | sort -u | while read -r p; do
  b=$(blob "$B" "$p"); l=$(blob "$L" "$p"); d=$(blob "$D" "$p"); m=$(blob "$M" "$p")
  lc=$([ "$l" != "$b" ] && echo 1 || echo 0); dc=$([ "$d" != "$b" ] && echo 1 || echo 0)
  if [ "$lc$dc" = 00 ]; then echo "INJECTED $p"; continue; fi
  if [ "$m" = "$l" ] && [ "$m" = "$d" ]; then c=SAME_BOTH
  elif [ "$m" = "$l" ] && [ "$dc" = 0 ]; then c=LANE_ONLY
  elif [ "$m" = "$d" ] && [ "$lc" = 0 ]; then c=DEV_ONLY
  elif [ "$lc$dc" = 11 ]; then c=BOTH_CHANGED_MERGED
  else c=UNEXPECTED; fi
  echo "$c $p"
done
