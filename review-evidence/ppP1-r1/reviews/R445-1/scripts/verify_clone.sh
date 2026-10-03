#!/bin/sh
# R445-1: prove the review clone is at the exact head with untouched tracked
# bytes, modes and index, and list its gitlinks. Usage: verify_clone.sh CLONE SHA TREE
set -e
c=$1; sha=$2; tree=$3
cd "$c"
echo "HEAD $(git rev-parse HEAD) (want $sha)"
echo "tree $(git rev-parse HEAD^{tree}) (want $tree)"
echo "porcelain lines (untracked included): $(git status --porcelain --untracked-files=all | wc -l)"
git diff --quiet HEAD -- && echo "worktree == HEAD: yes"
git diff --cached --quiet HEAD -- && echo "index == HEAD: yes"
# every tracked path: index mode/blob equals the tree's, and the worktree file hashes to it
git ls-files -s | awk '{print $1, $2, $4}' | sort > /tmp/r445_idx.$$
git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sort > /tmp/r445_tree.$$
cmp -s /tmp/r445_idx.$$ /tmp/r445_tree.$$ && echo "index entries == tree entries: $(wc -l < /tmp/r445_tree.$$)"
bad=0
git ls-files -s | while read mode blob stage path; do
  [ "$mode" = 160000 ] && continue
  h=$(git hash-object --no-filters -- "$path")
  [ "$h" = "$blob" ] || { echo "BLOB MISMATCH $path"; bad=1; }
  m=$( [ -x "$path" ] && echo 100755 || echo 100644 ); [ -L "$path" ] && m=120000
  [ "$m" = "$mode" ] || echo "MODE MISMATCH $path $m $mode"
done
echo "gitlinks (160000 entries): $(git ls-files -s | awk '$1==160000' | wc -l)"
rm -f /tmp/r445_idx.$$ /tmp/r445_tree.$$
