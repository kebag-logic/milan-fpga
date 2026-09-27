#!/usr/bin/env bash
# Re-hash every tracked working-tree file of a checkout and compare the blob id
# and mode with the exact head commit; also list gitlinks and stray files.
# Usage: verify_tree_bytes.sh <checkout> <expected-head> <expected-tree>
set -u
cd "$1" || exit 2
fail=0
[ "$(git rev-parse HEAD)" = "$2" ] || { echo "HEAD mismatch"; fail=1; }
[ "$(git rev-parse HEAD^{tree})" = "$3" ] || { echo "tree mismatch"; fail=1; }
n=0
while read -r mode _type blob path; do
  n=$((n + 1))
  if [ "$mode" = 160000 ]; then echo "gitlink $path $blob"; continue; fi
  got=$(git hash-object --no-filters -- "$path")
  [ "$got" = "$blob" ] || { echo "BLOB MISMATCH $path"; fail=1; }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "MODE MISMATCH $path"; fail=1; }
  else [ ! -x "$path" ] || { echo "MODE MISMATCH $path"; fail=1; }; fi
done < <(git ls-tree -r HEAD)
[ "$(git ls-files -s | awk '{print $1, $2, $4}')" = "$(git ls-tree -r HEAD | awk '{print $1, $3, $4}')" ] \
  || { echo "INDEX differs from HEAD"; fail=1; }
extra=$(git status --porcelain --ignored)
[ -z "$extra" ] || { echo "untracked/ignored/modified entries:"; echo "$extra"; fail=1; }
echo "tracked entries checked: $n"
echo "gitlinks: $(git ls-tree -r HEAD | awk '$1=="160000"' | wc -l)"
echo "result: $([ $fail = 0 ] && echo MATCH || echo MISMATCH)"
exit $fail
