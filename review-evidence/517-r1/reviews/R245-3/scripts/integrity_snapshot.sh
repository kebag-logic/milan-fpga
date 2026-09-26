#!/bin/sh
# Print an integrity snapshot of a checkout: HEAD, tree, index records, worktree
# status, per-file hash of tracked bytes and the required submodule gitlinks.
set -eu
cd "$1"
echo "HEAD $(git rev-parse HEAD)"
echo "TREE $(git rev-parse HEAD^{tree})"
echo "INDEX-RECORDS $(git ls-files -s | sha256sum | cut -d' ' -f1)"
echo "INDEX-VS-HEAD $(git diff --cached --name-only | wc -l)"
echo "WORKTREE-VS-INDEX $(git diff --name-only | wc -l)"
echo "UNTRACKED-NOT-IGNORED $(git status --porcelain --untracked-files=all | grep -c '^??' || true)"
echo "WORKTREE-BLOBS $(git ls-files -s | awk '$1!="160000"{print $4}' | git hash-object --stdin-paths | sha256sum | cut -d' ' -f1)"
echo "HEAD-BLOBS $(git ls-files -s | awk '$1!="160000"{print $2}' | sha256sum | cut -d' ' -f1)"
echo "MODES $(git ls-files -s | awk '{print $1, $4}' | sha256sum | cut -d' ' -f1)"
git ls-files -s | awk '$1=="160000"{print "GITLINK", $2, $4}'
git submodule status | sed 's/^/SUBMODULE /'
