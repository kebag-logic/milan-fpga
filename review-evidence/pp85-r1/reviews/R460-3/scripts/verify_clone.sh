#!/bin/sh
# Verify the review clone still holds the exact head bytes: HEAD, tree, a clean
# index and worktree, every tracked blob's bytes and mode, and the gitlinks.
# usage: verify_clone.sh CLONE EXPECTED_HEAD EXPECTED_TREE
set -eu
clone=$1 head=$2 tree=$3
cd "$clone"
[ "$(git rev-parse HEAD)" = "$head" ] && echo "HEAD $head OK"
[ "$(git rev-parse 'HEAD^{tree}')" = "$tree" ] && echo "tree $tree OK"
git update-index -q --really-refresh >/dev/null 2>&1 || true
[ -z "$(git status --porcelain --untracked-files=all --ignored)" ] && echo "status: clean, no untracked or ignored files"
git diff --quiet && git diff --cached --quiet && echo "worktree and index match HEAD"
# index entries (mode, blob, path) equal HEAD's tree listing
[ "$(git ls-files -s | awk '{print $1, $2, $4}')" = "$(git ls-tree -r HEAD | awk '{print $1, $3, $4}')" ] \
  && echo "index modes/blobs equal HEAD tree ($(git ls-files | wc -l) entries)"
# rehash every tracked file from disk and compare with HEAD's blob
bad=0
git ls-tree -r HEAD | while read -r mode type blob path; do
  [ "$type" = blob ] || continue
  if [ "$mode" = 120000 ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin)
  else got=$(git hash-object "$path"); fi
  [ "$got" = "$blob" ] || { echo "BLOB MISMATCH $path"; exit 1; }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE MISMATCH $path"; exit 1; fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE MISMATCH $path"; exit 1; fi
done && echo "every tracked blob rehashes to HEAD's bytes, modes match"
n=$(git ls-files -s | awk '$1 == "160000"' | wc -l)
echo "gitlinks: $n (no .gitmodules: $( [ -e .gitmodules ] && echo present || echo absent))"
