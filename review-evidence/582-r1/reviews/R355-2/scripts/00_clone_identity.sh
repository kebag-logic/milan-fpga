#!/bin/bash
# Record the review clone's exact identity: head, tree, index, gitlinks, dirty state.
set -uo pipefail
C=${1:-$REVIEWS/r355-2-582}
cd "$C" || exit 2
echo "head $(git rev-parse HEAD 2>/dev/null)"
echo "tree $(git rev-parse 'HEAD^{tree}' 2>/dev/null)"
echo "index-tree $(git write-tree 2>/dev/null)"
echo "ls-files-stage-sha256 $(git ls-files -s 2>/dev/null | sha256sum | cut -d' ' -f1)"
echo "gitlinks:"; git ls-files -s 2>/dev/null | awk '$1=="160000"'
echo "status-porcelain-begin"; git status --porcelain=v1 --ignore-submodules=none 2>/dev/null; echo "status-porcelain-end"
echo "diff-head-rc $(git diff --quiet HEAD 2>/dev/null; echo $?)"
