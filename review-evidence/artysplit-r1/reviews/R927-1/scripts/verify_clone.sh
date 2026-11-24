#!/usr/bin/env bash
# Prove the review clone still holds the exact head: HEAD, tree, a clean
# index and worktree (tracked bytes and modes), and the submodule gitlinks.
# usage: verify_clone.sh <clone> <head-sha> <tree-sha>
set -u
c=$1 head=$2 tree=$3
cd "$c" || exit 2
echo "HEAD $(git rev-parse HEAD) want $head"
echo "TREE $(git rev-parse HEAD^{tree}) want $tree"
echo "INDEX-TREE $(git write-tree 2>/dev/null) want $tree"
echo "STATUS-PORCELAIN-LINES $(git status --porcelain --untracked-files=all | wc -l)"
git diff --quiet HEAD -- && echo "WORKTREE-DIFF none" || echo "WORKTREE-DIFF present"
git ls-files -v | awk '$1 != "H" {print "NONSTANDARD-INDEX-FLAG", $0}' | head -5
git ls-files --stage | awk '$1 == "160000" {print "GITLINK", $2, $4}'
git submodule status | sed 's/^/SUBMODULE /'
