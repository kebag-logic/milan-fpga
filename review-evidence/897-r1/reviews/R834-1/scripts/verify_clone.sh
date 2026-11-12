#!/bin/sh
# Verify the review clone is at the exact head with no tracked, index or gitlink drift.
# usage: verify_clone.sh <clone>
set -u
C=$1
cd "$C" || exit 2
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
echo "status --porcelain (untracked included):"; git status --porcelain --untracked-files=all | sed 's/^/  /'
git diff --quiet && echo "worktree == index: yes" || echo "worktree == index: NO"
git diff --cached --quiet && echo "index == HEAD: yes" || echo "index == HEAD: NO"
echo "index tree $(git write-tree)"
echo "gitlinks at HEAD vs checked-out submodules:"
git ls-tree -r HEAD | awk '$2=="commit"{print $3, $4}' | while read sha path; do
  if [ -e "$path/.git" ]; then got=$(git -C "$path" rev-parse HEAD 2>/dev/null); else got="(not initialised)"; fi
  [ "$got" = "$sha" ] && m=match || m="differs"; echo "  $path $sha checked-out=$got $m"
done
