#!/usr/bin/env bash
# Verify a review clone is byte-exact at a commit: HEAD, tree, clean status (ignored too),
# index == HEAD tree, every tracked file's on-disk blob hash and mode, and gitlinks.
# usage: clone_integrity.sh <repo> <commit>
set -u
cd "$1"; want=$2
echo "HEAD $(git rev-parse HEAD) want $want"; echo "tree $(git rev-parse 'HEAD^{tree}')"
echo "status --porcelain --ignored: [$(git status --porcelain --ignored | wc -l) lines]"; git status --porcelain --ignored | head
echo "index tree $(git write-tree) (equal to HEAD tree: $([ "$(git write-tree)" = "$(git rev-parse 'HEAD^{tree}')" ] && echo yes || echo NO))"
n=0; bad=0
while read -r mode blob stage path; do
  n=$((n+1))
  if [ "$mode" = 160000 ]; then echo "gitlink $path $blob"; continue; fi
  h=$(git hash-object --no-filters -- "$path")
  if [ "$mode" = 120000 ]; then h=$(printf '%s' "$(readlink -- "$path")" | git hash-object --stdin); fi
  [ "$h" = "$blob" ] || { bad=$((bad+1)); echo "BLOB MISMATCH $path"; }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then bad=$((bad+1)); echo "MODE MISMATCH $path"; fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then bad=$((bad+1)); echo "MODE MISMATCH $path"; fi
done < <(git ls-files -s)
echo "index entries $n, mismatches $bad"
echo "gitlinks: $(git ls-files -s | awk '$1==160000' | wc -l); .gitmodules: $([ -f .gitmodules ] && echo present || echo absent)"
