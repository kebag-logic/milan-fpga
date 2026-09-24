#!/bin/sh
# Verify a processor checkout is exactly the reviewed head: HEAD and tree,
# index entries (mode + blob) equal to the HEAD tree, every worktree file's
# bytes and mode equal to its index blob, no untracked or ignored files, and
# the gitlinks (none expected in the processor tree).
#   usage: verify_clone_state.sh <checkout> <expected-head> <expected-tree>
set -u
repo=$1; want_head=$2; want_tree=$3
cd "$repo" || exit 2
rc=0
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "head=$head tree=$tree"
[ "$head" = "$want_head" ] || { echo "HEAD MISMATCH"; rc=1; }
[ "$tree" = "$want_tree" ] || { echo "TREE MISMATCH"; rc=1; }
git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sort > /tmp/.r315-tree.$$
git ls-files -s | awk '{print $1, $2, $4}' | sort > /tmp/.r315-index.$$
if cmp -s /tmp/.r315-tree.$$ /tmp/.r315-index.$$; then
  echo "index == HEAD tree ($(wc -l < /tmp/.r315-index.$$) entries, modes and blobs)"
else
  echo "INDEX DIFFERS FROM HEAD TREE"; rc=1
fi
rm -f /tmp/.r315-tree.$$ /tmp/.r315-index.$$
# worktree bytes: re-hash every tracked file and compare with its index blob
bad=0
git ls-files -s | while read -r mode blob stage path; do
  if [ "$mode" = 160000 ]; then continue; fi
  actual=$(git hash-object --no-filters -- "$path")
  [ "$actual" = "$blob" ] || { echo "BYTES DIFFER: $path"; exit 1; }
  if [ "$mode" = 100755 ]; then [ -x "$path" ] || { echo "MODE DIFFERS: $path"; exit 1; }
  else [ ! -x "$path" ] || { echo "MODE DIFFERS: $path"; exit 1; }; fi
done || bad=1
[ $bad = 0 ] && echo "worktree bytes and modes == index" || rc=1
extra=$(git status --porcelain --ignored --untracked-files=all | wc -l)
echo "untracked/ignored/modified entries: $extra"
[ "$extra" = 0 ] || { git status --porcelain --ignored --untracked-files=all | head; rc=1; }
links=$(git ls-files -s | awk '$1 == 160000' | wc -l)
echo "gitlinks in tree: $links; .gitmodules present: $( [ -f .gitmodules ] && echo yes || echo no )"
echo "verify rc=$rc"
exit $rc
