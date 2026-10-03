#!/usr/bin/env bash
# R445-2: verify a review clone is byte-exact at the reviewed head after probes.
# Usage: clone_integrity.sh <repo> <head-sha> <tree-sha>
set -euo pipefail
cd "$1"; HEAD_SHA=$2; TREE=$3; rc=0
[ "$(git rev-parse HEAD)" = "$HEAD_SHA" ] && echo "HEAD ok $HEAD_SHA" || { echo "HEAD MISMATCH"; rc=1; }
[ "$(git rev-parse HEAD^{tree})" = "$TREE" ] && echo "tree ok $TREE" || { echo "TREE MISMATCH"; rc=1; }
[ "$(git write-tree)" = "$TREE" ] && echo "index tree ok" || { echo "INDEX MISMATCH"; rc=1; }
st=$(git status --porcelain --ignored --untracked-files=all)
[ -z "$st" ] && echo "porcelain (incl. ignored) empty" || { echo "PORCELAIN NOT EMPTY:"; echo "$st" | head; rc=1; }
n=0; bad=0
while read -r mode blob stage path; do
  n=$((n+1))
  if [ "$mode" = 160000 ]; then echo "gitlink $path $blob"; continue; fi
  h=$(git hash-object --no-filters -- "$path")
  fm=$(stat -c %a -- "$path"); case "$mode" in 100755) want=755;; 120000) want=link;; *) want=644;; esac
  [ -L "$path" ] && fm=link
  if [ "$h" != "$blob" ]; then echo "BLOB MISMATCH $path"; bad=$((bad+1)); fi
  if [ "$want" = 755 ] && [ "$fm" != 755 ]; then echo "MODE MISMATCH $path $fm"; bad=$((bad+1)); fi
  if [ "$want" = 644 ] && [ $((8#$fm & 8#111)) -ne 0 ]; then echo "MODE MISMATCH $path $fm"; bad=$((bad+1)); fi
done < <(git ls-files -s)
echo "index entries $n, mismatches $bad, gitlinks $(git ls-files -s | awk '$1==160000' | wc -l)"
[ "$bad" -eq 0 ] || rc=1
exit $rc
