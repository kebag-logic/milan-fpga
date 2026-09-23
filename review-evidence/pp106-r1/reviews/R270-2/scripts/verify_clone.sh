#!/usr/bin/env bash
# Verify a review clone is byte-exact at an expected head: HEAD/tree, index
# equal to the tree, every tracked file's bytes and mode equal to the index,
# no untracked or ignored leftovers, and the gitlink set.
# usage: verify_clone.sh <clone> <head> <tree>
set -uo pipefail
c=$1; h=$2; t=$3; rc=0
cd "$c" || exit 2
[ "$(git rev-parse HEAD)" = "$h" ] && echo "HEAD $h OK" || { echo "HEAD MISMATCH"; rc=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$t" ] && echo "tree $t OK" || { echo "TREE MISMATCH"; rc=1; }
[ "$(git write-tree)" = "$t" ] && echo "index == tree OK" || { echo "INDEX != TREE"; rc=1; }
git update-index -q --really-refresh >/dev/null 2>&1
if git diff-files --quiet; then echo "worktree bytes+modes == index OK"; else echo "WORKTREE DIFFERS"; git diff-files --name-status | head; rc=1; fi
n=0; bad=0
while read -r mode blob stage path; do
  n=$((n+1))
  [ "$mode" = 160000 ] && continue
  [ "$(git hash-object --no-filters -- "$path")" = "$blob" ] || { echo "BLOB MISMATCH $path"; bad=$((bad+1)); }
  fm=$(stat -c %a -- "$path"); want=${mode: -3}; [ "$want" = 644 ] || [ "$want" = 755 ] || want=$want
  { [ "$mode" = 100755 ] && [ -x "$path" ]; } || { [ "$mode" = 100644 ] && [ ! -x "$path" ]; } || [ "$mode" = 120000 ] || { echo "MODE MISMATCH $path $mode $fm"; bad=$((bad+1)); }
done < <(git ls-files -s | tr '\t' ' ')
echo "$n tracked entries re-hashed, $bad mismatches"; [ "$bad" = 0 ] || rc=1
u=$(git status --porcelain=v1 --untracked-files=all --ignored | wc -l)
echo "status entries (untracked/ignored/modified): $u"; [ "$u" = 0 ] || rc=1
echo "gitlinks: $(git ls-files -s | awk '$1=="160000"' | wc -l) $(git ls-files -s | awk '$1=="160000"{print $2, $4}')"
echo "index sha256: $(git ls-files -s | sha256sum | cut -d' ' -f1)"
exit $rc
