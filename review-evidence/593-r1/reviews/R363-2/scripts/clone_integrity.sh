#!/bin/sh
# R363-1/R363-2: prove the review clone still equals the exact head after all probes.
# Usage: clone_integrity.sh <repo-root> <head-sha> <tree-sha>
set -u
repo=$1; head=$2; tree=$3
cd "$repo" || exit 2
echo "HEAD $(git rev-parse HEAD) expect $head"
echo "tree $(git rev-parse HEAD^{tree}) expect $tree"
echo "index-tree $(git write-tree) expect $tree"
echo "status (porcelain, incl. untracked and ignored):"
git status --porcelain --ignored | sed 's/^/  /'
echo "flags (assume-unchanged/skip-worktree):"
git ls-files -v | grep -E '^[a-z]|^S' | sed 's/^/  /' || true
mism=0; n=0
git ls-files -s | while read -r mode sha stage path; do
  if [ "$mode" = 160000 ]; then continue; fi
  n=$((n+1))
  got=$(git hash-object --no-filters -- "$path" 2>/dev/null || echo missing)
  [ "$got" = "$sha" ] || { echo "  BLOB MISMATCH $path"; }
  if [ -x "$path" ]; then fm=100755; else fm=100644; fi
  [ -L "$path" ] && fm=120000
  [ "$fm" = "$mode" ] || echo "  MODE MISMATCH $path $fm != $mode"
done
echo "blob/mode scan done (mismatch lines above, none means clean)"
echo "gitlinks:"
git ls-files -s | awk '$1==160000{print "  "$2" "$4}'
git ls-tree -r HEAD | awk '$1==160000{print "  tree "$3" "$4}'
