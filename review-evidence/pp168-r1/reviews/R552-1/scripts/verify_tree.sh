#!/usr/bin/env bash
# Verify the review clone is byte-exact at the expected head: HEAD, tree, index == HEAD tree,
# every tracked worktree blob hash and mode == index, no submodule gitlinks expected or present.
set -u
repo=$1 head=$2 tree=$3; cd "$repo" || exit 2
rc=0
[ "$(git rev-parse HEAD)" = "$head" ] || { echo "HEAD mismatch"; rc=1; }
[ "$(git rev-parse HEAD^{tree})" = "$tree" ] || { echo "tree mismatch"; rc=1; }
[ "$(git write-tree)" = "$tree" ] || { echo "index tree mismatch"; rc=1; }
git diff --quiet || { echo "worktree differs from index"; rc=1; }
git diff --cached --quiet || { echo "index differs from HEAD"; rc=1; }
bad=0; n=0
while read -r mode obj stage path; do
  n=$((n+1))
  if [ "$mode" = 160000 ]; then echo "gitlink $path $obj"; continue; fi
  h=$(git hash-object --no-filters -- "$path") || { echo "unreadable $path"; bad=$((bad+1)); continue; }
  [ "$h" = "$obj" ] || { echo "blob mismatch $path"; bad=$((bad+1)); }
  if [ -L "$path" ]; then m=120000; elif [ -x "$path" ]; then m=100755; else m=100644; fi
  [ "$m" = "$mode" ] || { echo "mode mismatch $path $m != $mode"; bad=$((bad+1)); }
done < <(git ls-files -s)
gl=$(git ls-tree -r HEAD | awk '$1=="160000"' | wc -l)
echo "tracked=$n blob/mode mismatches=$bad gitlinks_in_head=$gl untracked_not_ignored=$(git status --porcelain --untracked-files=all | wc -l)"
[ "$bad" = 0 ] || rc=1
echo "verify rc=$rc"; exit $rc
