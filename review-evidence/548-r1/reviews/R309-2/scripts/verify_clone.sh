#!/bin/sh
# Verify a review clone sits at the exact head with clean tracked bytes, modes, index and gitlinks.
# Usage: verify_clone.sh <clone> <head-sha> <tree-sha>
set -eu
C=$1; H=$2; T=$3
cd "$C"
test "$(git rev-parse HEAD)" = "$H" && echo "HEAD $H OK"
test "$(git rev-parse HEAD^{tree})" = "$T" && echo "TREE $T OK"
test "$(git write-tree)" = "$T" && echo "INDEX tree == $T OK"
git diff --quiet HEAD && git diff --cached --quiet && echo "worktree+index vs HEAD: no diff (bytes and modes)"
test -z "$(git status --porcelain --untracked-files=all)" && echo "status porcelain: empty"
git ls-files -s | awk '$1=="160000"{print "gitlink index", $2, $4}'
git ls-tree -r HEAD | awk '$2=="commit"{print "gitlink HEAD ", $3, $4}'
git submodule status | sed 's/^/submodule /'
