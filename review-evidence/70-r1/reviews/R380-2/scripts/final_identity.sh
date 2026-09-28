#!/bin/sh
# Final clone identity: HEAD, tree, index-vs-HEAD entries, worktree status,
# gitlinks and submodule checkouts. Run from the parent repository root.
set -u
echo "date: $(date -u +%FT%TZ)"
echo "HEAD $(git rev-parse HEAD)"
echo "tree $(git rev-parse 'HEAD^{tree}')"
echo "index file sha256 $(sha256sum "$(git rev-parse --git-dir)/index" | cut -d' ' -f1)"
a=$(git ls-files -s | awk '{print $1, $2, $4}' | sha256sum | cut -d' ' -f1)
b=$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sha256sum | cut -d' ' -f1)
echo "index entries (mode blob path) sha256 $a"
echo "HEAD tree entries (mode blob path) sha256 $b"
[ "$a" = "$b" ] && echo "index==HEAD: YES" || echo "index==HEAD: NO"
git diff --quiet && echo "worktree vs index: clean" || echo "worktree vs index: DIRTY"
git diff --cached --quiet && echo "index vs HEAD: clean" || echo "index vs HEAD: DIRTY"
echo "porcelain entries: $(git status --porcelain=v1 --untracked-files=all | wc -l)"
git ls-tree -r HEAD | awk '$2=="commit"'
git submodule status 2>/dev/null
echo "processor porcelain entries: $(git -C protocol-processor status --porcelain | wc -l)"
