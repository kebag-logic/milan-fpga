#!/usr/bin/env bash
# Reviewer check (R469-3): the head merge f9b8f0e is the mechanical union of
# its two parents: every path either parent changed since their merge base
# carries that parent's blob at the head, no path is changed by both, and no
# other path differs from the base.  usage: check_merge_union.sh <clone>
set -eu
cd "$1"
H=f9b8f0ee6604a73b9fa82c62b91811e9f53b320a
L=$(git rev-parse "$H^1"); M=$(git rev-parse "$H^2"); MB=$(git merge-base "$L" "$M")
echo "head $H lane-parent $L main-parent $M merge-base $MB"
A=$(git diff --name-only "$MB" "$L" | sort); B=$(git diff --name-only "$MB" "$M" | sort)
echo "lane-side paths: $(echo "$A" | grep -c .)  main-side paths: $(echo "$B" | grep -c .)"
echo "paths changed by both: $(comm -12 <(echo "$A") <(echo "$B") 2>/dev/null | grep -c . || true)"
bad=0
for f in $A; do [ "$(git rev-parse "$H:$f" 2>/dev/null || echo gone)" = "$(git rev-parse "$L:$f" 2>/dev/null || echo gone)" ] || { echo "MISMATCH lane $f"; bad=1; }; done
for f in $B; do [ "$(git rev-parse "$H:$f" 2>/dev/null || echo gone)" = "$(git rev-parse "$M:$f" 2>/dev/null || echo gone)" ] || { echo "MISMATCH main $f"; bad=1; }; done
extra=$(git diff --name-only "$MB" "$H" | sort | grep -vxF -f <(printf '%s\n%s\n' "$A" "$B") || true)
echo "paths differing from base outside both sides: $(echo "$extra" | grep -c . || true)"
echo "lane-only diff vs main-parent: $(git diff --name-only "$M" "$H" | grep -c .) paths"
git diff --stat "$M" "$H" | tail -1
echo "RESULT: $([ $bad = 0 ] && [ -z "$extra" ] && echo UNION || echo NOT-UNION)"
