#!/bin/sh
# replay_merge.sh <clone>: replays the round-2 merge and classifies the delta.
# 1. git merge-tree recomputes the conflicts of 1105f545 + 1eb5289d.
# 2. The merge commit is compared with the clean auto-merge tree: only the
#    conflicted files and STRICTER_READINGS.md (the stated semantic edit) differ.
# 3. Every file changed in 1105f545..HEAD is classed dev-side / pr-side / combined.
set -eu
cd "$1"
T=$(git merge-tree --write-tree --name-only 1105f545 1eb5289d | head -1 || true)
echo "auto-merge tree $T"
git merge-tree --write-tree --name-only 1105f545 1eb5289d | sed -n '2,/^$/p' || true
echo "--- merge commit 04148cd764 vs auto-merge tree"
git diff --stat "$T" 04148cd764 | tail -12
echo "--- first-parent commits after the merge"
for c in $(git rev-list --first-parent 04148cd764..HEAD); do
  git show --stat --format='%h' "$c" | sed -n '1p;3,$p'
done
echo "--- 1105f545..HEAD classes"
for f in $(git diff --name-only 1105f545 HEAD); do
  h=$(git rev-parse -q --verify "HEAD:$f" 2>/dev/null || true)
  d=$(git rev-parse -q --verify "1eb5289d:$f" 2>/dev/null || true)
  p=$(git rev-parse -q --verify "1105f545:$f" 2>/dev/null || true)
  if [ "$h" = "$d" ]; then c=dev-side; elif [ "$h" = "$p" ]; then c=pr-side; else c=combined; fi
  echo "$c $f"
done
