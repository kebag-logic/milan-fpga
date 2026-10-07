#!/bin/sh
# Usage: integrity.sh CLONE  -- verify exact head, tree, index, tracked bytes and modes, gitlinks.
cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD)"
echo "tree $(git rev-parse HEAD^{tree})"
echo "index-tree $(git write-tree)"
git update-index -q --really-refresh
git diff --quiet HEAD -- && echo "worktree==HEAD bytes/modes: yes" || echo "worktree==HEAD bytes/modes: NO"
git diff --cached --quiet HEAD -- && echo "index==HEAD: yes" || echo "index==HEAD: NO"
echo "untracked: $(git status --porcelain --untracked-files=all | wc -l)"
echo "gitlinks: $(git ls-files -s | awk '$1=="160000"' | wc -l)"
bad=0; git ls-tree -r HEAD | while read m t h p; do [ "$(git hash-object "$p")" = "$h" ] || echo "BLOB MISMATCH $p"; done
echo "tracked files: $(git ls-files | wc -l)"
