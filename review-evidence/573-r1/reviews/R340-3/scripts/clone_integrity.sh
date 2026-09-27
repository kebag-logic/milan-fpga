#!/usr/bin/env bash
# Prove the review clone still holds the exact head: HEAD/tree/write-tree,
# a clean porcelain, index modes/blobs equal to the HEAD tree, worktree blob
# bytes equal to HEAD blobs, and the submodule gitlinks.
# Usage: clone_integrity.sh <clone> <expected head> <expected tree>
set -euo pipefail
cd "$1"
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "HEAD $head tree $tree"
test "$head" = "$2" && test "$tree" = "$3" && echo "HEAD/tree == expected"
echo "porcelain-lines $(git status --porcelain --ignore-submodules=none | wc -l)"
echo "write-tree $(git write-tree)"
diff <(git ls-files -s | awk '{print $1, $2, $4}') \
     <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') && echo "index modes/blobs == HEAD tree ($(git ls-files -s | wc -l) entries)"
git diff --quiet && git diff --cached --quiet && echo "worktree==index==HEAD (git diff)"
# rehash every regular tracked file from the worktree bytes
wt=$(git ls-files -s | awk '$1 != "160000" {print $4}' | git hash-object --stdin-paths | sha256sum)
hd=$(git ls-tree -r HEAD | awk '$1 != "160000" {print $3}' | sha256sum)
echo "worktree-blob-list-sha256 $wt"; echo "HEAD-blob-list-sha256     $hd"
test "$wt" = "$hd" && echo "worktree blob bytes == HEAD blobs"
git ls-tree -r HEAD | awk '$1 == "160000"'
git submodule status
