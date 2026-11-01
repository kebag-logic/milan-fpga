#!/bin/sh
# usage: recompute_conflicts.sh <clone> <base-line> <dev> <merge> <outdir>: the auto-merged tree, its conflicted files, each file's hunk count, and its diff to the merge commit.
set -eu
c=$1; a=$2; b=$3; m=$4; o=$5
cd "$c"
git merge-tree --write-tree --name-only --messages "$a" "$b" > "$o/merge-tree-names.txt" || true
t=$(head -1 "$o/merge-tree-names.txt")
git diff --no-color "$t" "$m" > "$o/merge-autotree-to-97e9a3d3.diff"
total=0
for f in $(sed -n '2,/^$/p' "$o/merge-tree-names.txt"); do
  n=$(git show "$t:$f" | grep -c '^<<<<<<< ' || true); total=$((total+n)); echo "$f $n"
done > "$o/merge-conflict-hunks.txt"
echo "files $(wc -l < "$o/merge-conflict-hunks.txt") hunks $total" >> "$o/merge-conflict-hunks.txt"
git diff --name-only "$t" "$m" | sort > "$o/merge-resolved-files.txt"
