#!/bin/sh
# Reviewer check: the review clone still holds the exact published head,
# with a clean worktree and index, every tracked blob's bytes and mode equal
# to HEAD's, and (this repository has none) no submodule gitlinks to restore.
# Usage: verify_clone.sh CLONE EXPECTED_HEAD EXPECTED_TREE
clone=$1; head=$2; tree=$3
cd "$clone" || exit 2
rc=0
h=$(git rev-parse HEAD); t=$(git rev-parse HEAD^{tree})
echo "HEAD $h"; echo "tree $t"
[ "$h" = "$head" ] || { echo "FAIL head"; rc=1; }
[ "$t" = "$tree" ] || { echo "FAIL tree"; rc=1; }
st=$(git status --porcelain --untracked-files=all --ignored)
[ -z "$st" ] && echo "status: clean (no untracked, no ignored)" || { echo "FAIL status:"; echo "$st"; rc=1; }
git diff --quiet --exit-code && echo "worktree == index" || { echo "FAIL worktree"; rc=1; }
git diff --cached --quiet --exit-code && echo "index == HEAD" || { echo "FAIL index"; rc=1; }
# index entries (mode, blob) against HEAD's tree, entry by entry
a=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum)
b=$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sha256sum)
[ "$a" = "$b" ] && echo "index modes/blobs == HEAD tree ($(git ls-files | wc -l) entries)" || { echo "FAIL index/tree entries"; rc=1; }
# worktree bytes rehashed against the index
bad=0
git ls-files -s | while read -r mode blob stage path; do
  [ "$mode" = 160000 ] && continue
  w=$(git hash-object --no-filters -- "$path")
  [ "$w" = "$blob" ] || { echo "FAIL bytes $path"; echo x; }
done > /tmp/.verify_clone_$$ 2>&1
if [ -s /tmp/.verify_clone_$$ ]; then cat /tmp/.verify_clone_$$; rc=1; else echo "every tracked blob's bytes rehash to HEAD"; fi
rm -f /tmp/.verify_clone_$$
g=$(git ls-files -s | awk '$1=="160000"' | wc -l)
echo "submodule gitlinks: $g"
echo "rc=$rc"
exit $rc
