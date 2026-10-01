#!/bin/sh
# Verify the reviewed clone is still exactly the published head: HEAD, HEAD
# tree, index tree, no worktree or ignored drift, every tracked blob rehashes
# to its index id with its index mode, no index flags, and the gitlinks.
# Usage: tree_integrity.sh CLONE HEAD_SHA TREE_SHA
set -u
C=$1; H=$2; T=$3
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) (want $H)"
echo "HEAD^{tree} $(git rev-parse 'HEAD^{tree}') (want $T)"
echo "index tree $(git write-tree) (want $T)"
echo "symbolic-ref: $(git symbolic-ref -q HEAD || echo detached)"
echo "status --porcelain --ignored: [$(git status --porcelain --ignored | wc -l) lines]"
git status --porcelain --ignored | head -5
bad=0; n=0
git ls-files -s | while read -r mode oid stage path; do
  [ "$mode" = 160000 ] && { echo "gitlink $path $oid"; continue; }
  got=$(git hash-object --no-filters -- "$path")
  [ "$got" = "$oid" ] || echo "BLOB MISMATCH $path"
  if [ -L "$path" ]; then fm=120000; elif [ -x "$path" ]; then fm=100755; else fm=100644; fi
  [ "$fm" = "$mode" ] || echo "MODE MISMATCH $path $mode $fm"
done
echo "tracked entries: $(git ls-files -s | wc -l), gitlinks: $(git ls-files -s | awk '$1==160000' | wc -l)"
echo "flags (assume-unchanged h/skip-worktree S): $(git ls-files -v | grep -c '^[hS]')"
