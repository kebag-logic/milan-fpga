#!/usr/bin/env bash
# Confirm a review clone still holds the exact head bytes after probes.
# Usage: restore_check.sh <repo> <expected-head> <expected-tree>
set -u
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD) expected $2"
echo "tree $(git rev-parse 'HEAD^{tree}') expected $3"
echo "index-tree $(git write-tree)"
echo "diff-worktree-vs-index: $(git diff --name-only | wc -l) files; mode changes: $(git diff --summary | grep -c 'mode change')"
echo "diff-index-vs-HEAD: $(git diff --cached --name-only | wc -l) files"
echo "untracked: $(git ls-files --others --exclude-standard | wc -l); ignored: $(git ls-files --others --ignored --exclude-standard | wc -l)"
echo "gitlinks:"; git ls-tree -r HEAD | awk '$2 == "commit" {print "  " $3, $4}'
echo "submodule status:"; git submodule status | sed 's/^/  /'
