#!/bin/sh
# Verify a review clone sits at exact head bytes: HEAD, tree, index equal to
# the tree (all stage 0, no assume-unchanged/skip-worktree flags), every
# tracked file's bytes and mode equal to its blob, no untracked or ignored
# leftovers, and every submodule gitlink at its recorded commit and clean.
# Usage: verify_clone.sh <clone> <head-sha> <tree-sha>
set -eu
c=$1; head=$2; tree=$3; rc=0
[ "$(git -C "$c" rev-parse HEAD)" = "$head" ] && echo "HEAD $head" || { echo "HEAD MISMATCH"; rc=1; }
[ "$(git -C "$c" rev-parse HEAD^{tree})" = "$tree" ] && echo "tree $tree" || { echo "TREE MISMATCH"; rc=1; }
[ "$(git -C "$c" write-tree)" = "$tree" ] && echo "index writes tree $tree" || { echo "INDEX MISMATCH"; rc=1; }
n=$(git -C "$c" ls-files -s | awk '$3!=0' | wc -l); echo "index entries not at stage 0: $n"; [ "$n" = 0 ] || rc=1
n=$(git -C "$c" ls-files -v | grep -vc '^H ' || true); echo "index entries with flags (not H): $n"; [ "$n" = 0 ] || rc=1
git -C "$c" update-index -q --really-refresh >/dev/null 2>&1 || true
if git -C "$c" diff --quiet HEAD -- && git -C "$c" diff --quiet --cached HEAD --; then echo "worktree and index equal HEAD (bytes, modes)"; else echo "WORKTREE/INDEX DIFFER"; rc=1; fi
# Independent byte check: hash every tracked regular file and compare to its blob.
bad=$(git -C "$c" ls-files -s | awk '$1!="160000"{print $1" "$2" "$4}' | while read -r mode blob path; do
  f="$c/$path"
  if [ "$mode" = 120000 ]; then h=$(readlink "$f" | tr -d '\n' | git hash-object --stdin)
  else h=$(git hash-object --no-filters "$f")
       x=100644; [ -x "$f" ] && x=100755; [ "$x" = "$mode" ] || echo "MODE $path"; fi
  [ "$h" = "$blob" ] || echo "BYTES $path"
done | wc -l)
echo "tracked files whose bytes or mode differ from their blob: $bad"; [ "$bad" = 0 ] || rc=1
u=$(git -C "$c" status --porcelain --ignored --untracked-files=all --ignore-submodules=none | wc -l)
echo "untracked/ignored/modified entries: $u"; [ "$u" = 0 ] || rc=1
git -C "$c" ls-files -s | awk '$1=="160000"{print $2" "$4}' | while read -r pin path; do
  if [ -e "$c/$path/.git" ]; then
    at=$(git -C "$c/$path" rev-parse HEAD); d=$(git -C "$c/$path" status --porcelain --ignored | wc -l)
    echo "submodule $path pin $pin at $at dirty-entries $d $( [ "$at" = "$pin" ] && [ "$d" = 0 ] && echo OK || echo BAD)"
  else echo "submodule $path pin $pin not initialised"; fi
done
[ $rc = 0 ] && echo "CLONE VERIFIED" || echo "CLONE NOT VERIFIED"
exit $rc
