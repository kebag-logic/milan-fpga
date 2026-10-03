#!/bin/sh
# Usage: clone_integrity.sh <clone> <head> <tree>
# Verifies HEAD and tree, an empty status (ignored files included), index tree == HEAD tree,
# every tracked file's on-disk blob hash and executable bit against the index, and gitlinks.
set -u
cd "$1" || exit 2
echo "HEAD=$(git rev-parse HEAD) want=$2"
echo "TREE=$(git rev-parse 'HEAD^{tree}') want=$3"
echo "index_tree=$(git write-tree)"
echo "status_porcelain_ignored_lines=$(git status --porcelain --ignored | wc -l)"
git ls-files -s > /tmp/.ci_idx.$$
total=0; bad=0
while read -r mode blob stage path; do
  total=$((total+1))
  case "$mode" in
    160000) echo "GITLINK $path $blob"; continue;;
    120000) h=$(readlink -- "$path" | tr -d '\n' | git hash-object --stdin);;
    *) h=$(git hash-object -- "$path");;
  esac
  [ "$h" = "$blob" ] || { echo "BLOB MISMATCH $path"; bad=$((bad+1)); }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE MISMATCH $path"; bad=$((bad+1)); fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE MISMATCH $path"; bad=$((bad+1)); fi
done < /tmp/.ci_idx.$$
rm -f /tmp/.ci_idx.$$
echo "index_entries=$total mismatches=$bad gitlinks=$(git ls-files -s | awk '$1==160000' | wc -l) gitmodules=$(test -f .gitmodules && echo yes || echo no)"
