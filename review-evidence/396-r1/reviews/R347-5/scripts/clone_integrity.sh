#!/usr/bin/env bash
# R347-5 clone integrity. Usage: clone_integrity.sh <repo-root>
# Confirms exact head/tree, clean index and worktree, tracked blob bytes and
# modes equal to HEAD, and every gitlink recorded in HEAD's tree.
set -u
cd "$1" || exit 2
want_head=07f72ad640f99c43bc1354642ad4d7ed8ba410cc
want_tree=d1b61e4301b6cd7fcf6d2536329cb329d6ae5c67
rc=0
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $head"; echo "TREE $tree"
[ "$head" = "$want_head" ] || { echo "HEAD MISMATCH"; rc=1; }
[ "$tree" = "$want_tree" ] || { echo "TREE MISMATCH"; rc=1; }
git diff --quiet || { echo "WORKTREE DIFFERS FROM INDEX"; rc=1; }
git diff --cached --quiet || { echo "INDEX DIFFERS FROM HEAD"; rc=1; }
st=$(git status --porcelain=v1 --untracked-files=all --ignore-submodules=none)
[ -z "$st" ] && echo "status: clean" || { echo "status: $st"; rc=1; }
# Rehash every tracked regular file and compare blob id and mode to HEAD.
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; oid=${rest#* }
  [ "$type" = blob ] || continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then
    [ -L "$path" ] && [ "$(printf %s "$(readlink "$path")" | git hash-object --stdin)" = "$oid" ] || { echo "SYMLINK $path"; bad=$((bad+1)); }
    continue
  fi
  [ "$(git hash-object --no-filters -- "$path")" = "$oid" ] || { echo "BYTES $path"; bad=$((bad+1)); }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "MODE $path"; bad=$((bad+1)); }
  else [ ! -x "$path" ] || { echo "MODE $path"; bad=$((bad+1)); }; fi
done < <(git ls-tree -r --full-tree HEAD)
echo "tracked blobs checked: $n, mismatches: $bad"
[ "$bad" -eq 0 ] || rc=1
echo "gitlinks in HEAD tree:"
git ls-tree -r HEAD | awk '$1=="160000"{print "  " $3 "  " $4}'
echo "submodule status (checked-out commit vs gitlink):"
git submodule status 2>&1 | sed 's/^/  /'
git submodule status 2>/dev/null | grep -E '^[+U]' && { echo "GITLINK MISMATCH"; rc=1; }
echo "integrity rc=$rc"
exit $rc
