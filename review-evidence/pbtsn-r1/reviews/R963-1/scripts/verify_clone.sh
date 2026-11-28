#!/bin/bash
# Verify a clone is at the exact reviewed head: HEAD, tree, index, every tracked blob's bytes and mode, gitlinks.
# Usage: verify_clone.sh CLONE EXPECTED_HEAD EXPECTED_TREE
set -u
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD) expected $2"
echo "tree $(git rev-parse 'HEAD^{tree}') expected $3"
echo "index-tree $(git write-tree)"
echo "tracked changes against index or HEAD: $(git status --porcelain --untracked-files=no | wc -l)"
echo "untracked, non-ignored files: $(git status --porcelain --untracked-files=all | grep -c '^??')"
echo "ignored entries: $(git status --porcelain --ignored | grep '^!!' | tr '\n' ' ')"
echo "gitlinks (mode 160000): $(git ls-files -s | awk '$1==160000' | wc -l); .gitmodules: $(test -f .gitmodules && echo present || echo absent)"
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  read -r mode oid stage <<< "$meta"
  n=$((n+1))
  h=$(git hash-object --no-filters -- "$path")
  [ "$h" = "$oid" ] || { bad=$((bad+1)); echo "BLOB MISMATCH $path"; }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { bad=$((bad+1)); echo "MODE MISMATCH $path"; }
  else [ ! -x "$path" ] || { bad=$((bad+1)); echo "MODE MISMATCH $path"; }; fi
done < <(git ls-files -s)
echo "tracked files checked: $n, blob or mode mismatches: $bad"
[ "$(git rev-parse HEAD)" = "$2" ] && [ "$(git rev-parse 'HEAD^{tree}')" = "$3" ] && [ "$(git write-tree)" = "$3" ] && [ "$bad" = 0 ]
