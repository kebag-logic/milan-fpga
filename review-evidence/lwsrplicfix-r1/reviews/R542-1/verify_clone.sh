#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Verify a clone sits at the exact head with untouched tracked bytes, modes and index.
# Usage: verify_clone.sh <repo> <head> <tree>
set -u
repo=$1; head=$2; tree=$3
cd "$repo" || exit 2
echo "HEAD=$(git rev-parse HEAD) expect=$head"
echo "TREE=$(git rev-parse 'HEAD^{tree}') expect=$tree"
echo "INDEX_TREE=$(git write-tree) expect=$tree"
git update-index -q --really-refresh
git diff --quiet HEAD -- && echo "worktree-vs-head: clean" || echo "worktree-vs-head: DIRTY"
git diff --cached --quiet && echo "index-vs-head: clean" || echo "index-vs-head: DIRTY"
echo "untracked+ignored:"; git status --porcelain --ignored --untracked-files=all
echo "gitlinks: $(git ls-files -s | awk '$1==160000' | wc -l)"
bad=0
git ls-files -s | while read -r mode obj stage path; do
    h=$(git hash-object --no-filters -- "$path")
    [ "$h" = "$obj" ] || { echo "BLOB MISMATCH $path"; }
    if [ "$mode" = 100755 ]; then [ -x "$path" ] || echo "MODE MISMATCH $path"; else [ ! -x "$path" ] || echo "MODE MISMATCH $path"; fi
done
echo "blob/mode check done for $(git ls-files | wc -l) files"
