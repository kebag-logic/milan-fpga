#!/usr/bin/env bash
# Verify a reviewed clone is at the exact head with tracked bytes, modes, index
# and gitlinks intact and nothing untracked or ignored left behind.
# Usage: clone_integrity.sh <clone> <head-sha> <tree-sha>
set -uo pipefail
cd "$1"; head=$2 tree=$3
echo "HEAD=$(git rev-parse HEAD) expected=$head"
echo "tree=$(git rev-parse HEAD^{tree}) expected=$tree"
echo "index-tree=$(git write-tree) (must equal tree)"
git diff-index --quiet HEAD -- && echo "diff-index HEAD: clean" || { echo "diff-index HEAD: DIRTY"; git diff-index HEAD --; }
n=0 bad=0
while read -r mode blob stage path; do
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin)
  else got=$(git hash-object --no-filters -- "$path"); fi
  fmode=100644; [ -x "$path" ] && fmode=100755; [ -L "$path" ] && fmode=120000
  if [ "$got" != "$blob" ] || [ "$fmode" != "$mode" ]; then bad=$((bad+1)); echo "MISMATCH $mode/$fmode $path"; fi
done < <(git ls-files -s)
echo "tracked blobs re-hashed: $n, mismatches: $bad"
git ls-files -s | awk '$1==160000 {print "gitlink " $4 " " $2}' | while read -r _ p s; do
  if [ -e "$p/.git" ]; then echo "gitlink $p index=$s checkout=$(git -C "$p" rev-parse HEAD) dirty=$(git -C "$p" status --porcelain | wc -l)"
  else echo "gitlink $p index=$s (uninitialised)"; fi
done
echo "untracked+ignored in superproject: $(git status --porcelain --ignored --ignore-submodules=all | wc -l)"
git status --porcelain --ignored --ignore-submodules=all | head
