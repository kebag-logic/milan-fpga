#!/usr/bin/env bash
# merge_check.sh REPO MERGE : re-derive a two-parent merge. For every path the
# merge differs from its merge base in, report which side(s) changed it and
# whether the merge's blob equals the one side that did; then git merge-tree's
# own result and its conflicts.
set -u
R=$1; M=$2
P1=$(git -C "$R" rev-parse "$M^1"); P2=$(git -C "$R" rev-parse "$M^2"); B=$(git -C "$R" merge-base "$P1" "$P2")
echo "merge $M  parent1 $P1  parent2 $P2  base $B"
git -C "$R" diff --name-only "$B" "$M" | while read -r f; do
  bb=$(git -C "$R" rev-parse -q --verify "$B:$f" 2>/dev/null || echo none)
  b1=$(git -C "$R" rev-parse -q --verify "$P1:$f" 2>/dev/null || echo none)
  b2=$(git -C "$R" rev-parse -q --verify "$P2:$f" 2>/dev/null || echo none)
  bm=$(git -C "$R" rev-parse -q --verify "$M:$f" 2>/dev/null || echo none)
  c1=$([ "$b1" != "$bb" ] && echo 1 || echo 0); c2=$([ "$b2" != "$bb" ] && echo 1 || echo 0)
  if [ $c1 = 1 ] && [ $c2 = 0 ]; then v=$([ "$bm" = "$b1" ] && echo "= parent1" || echo "DIFFERS from parent1")
  elif [ $c1 = 0 ] && [ $c2 = 1 ]; then v=$([ "$bm" = "$b2" ] && echo "= parent2" || echo "DIFFERS from parent2")
  else v="both sides changed"; fi
  echo "  $f: $v"
done
echo "merge-tree:"
git -C "$R" merge-tree --write-tree --name-only "$P1" "$P2" > /tmp/mt.$$ 2>&1; rc=$?
t=$(head -1 /tmp/mt.$$); echo "  rc=$rc tree=$t (merge's tree $(git -C "$R" rev-parse "$M^{tree}"))"; sed -n '2,$p' /tmp/mt.$$ | sed 's/^/  /'; rm -f /tmp/mt.$$
