#!/usr/bin/env bash
# Verifies a review clone is byte-identical to its exact head: HEAD, tree, clean status,
# index == HEAD tree, every tracked file's bytes and mode == the HEAD blob, gitlinks listed.
# usage: clone_verify.sh <clone> <head-sha> <tree-sha>
set -uo pipefail; cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD) (want $2)"; echo "tree $(git rev-parse HEAD^{tree}) (want $3)"
echo "status entries (incl. untracked/ignored): $(git status --porcelain --ignored | wc -l)"
echo "index vs HEAD: $(git diff-index --cached HEAD | wc -l) differing entries"
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  read -r mode _type blob <<<"$meta"
  [ "$mode" = 160000 ] && { echo "gitlink $path $blob"; continue; }
  n=$((n+1))
  if [ "$mode" = 120000 ]; then h=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin); else h=$(git hash-object --no-filters "$path"); fi
  fm=$(stat -c %a "$path"); want=644; [ "$mode" = 100755 ] && want=755
  { [ "$h" = "$blob" ] && { [ "$mode" = 120000 ] || [ "${fm: -3}" = "$want" ]; }; } || { bad=$((bad+1)); echo "MISMATCH $mode $path"; }
done < <(git ls-tree -r HEAD)
echo "tracked entries checked: $n, mismatching: $bad"; echo "gitlinks in HEAD: $(git ls-tree -r HEAD | grep -c '^160000' || true)"
[ "$(git rev-parse HEAD)" = "$2" ] && [ "$(git rev-parse HEAD^{tree})" = "$3" ] && [ $bad -eq 0 ]
