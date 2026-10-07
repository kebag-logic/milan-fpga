#!/usr/bin/env bash
# Verify a checkout is byte-exact at the expected head: HEAD, tree, index tree,
# every tracked blob's bytes and mode, gitlinks, and a clean status.
# Usage: verify_clone.sh CHECKOUT HEAD TREE
set -u
cd "$1" || exit 2
fail=0
[ "$(git rev-parse HEAD)" = "$2" ] && echo "HEAD ok $2" || { echo "HEAD MISMATCH"; fail=1; }
[ "$(git rev-parse HEAD^{tree})" = "$3" ] && echo "tree ok $3" || { echo "tree MISMATCH"; fail=1; }
[ "$(git write-tree)" = "$3" ] && echo "index tree ok" || { echo "index tree MISMATCH"; fail=1; }
n=0
while read -r mode type obj path; do
  n=$((n+1))
  if [ "$type" = commit ]; then echo "gitlink $path $obj"; continue; fi
  [ "$(git hash-object --no-filters -- "$path")" = "$obj" ] || { echo "BLOB MISMATCH $path"; fail=1; }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "MODE MISMATCH $path"; fail=1; }
  elif [ "$mode" = 100644 ]; then [ ! -x "$path" ] || { echo "MODE MISMATCH $path"; fail=1; }
  else echo "mode $mode $path"; fi
done < <(git ls-tree -r HEAD)
echo "tracked entries checked: $n"
echo "gitlinks: $(git ls-tree -r HEAD | awk '$2=="commit"' | wc -l); .gitmodules: $([ -e .gitmodules ] && echo present || echo absent)"
s=$(git status --porcelain --ignored); [ -z "$s" ] && echo "status clean (including ignored)" || { echo "STATUS NOT CLEAN"; echo "$s"; fail=1; }
echo "result: $([ $fail = 0 ] && echo PASS || echo FAIL)"; exit $fail
