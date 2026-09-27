#!/usr/bin/env bash
# Verify the review clone is byte-exact at the reviewed head. Usage: check_clone_integrity.sh <clone>
set -u; cd "$1" || exit 2
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
echo "status-porcelain(untracked+ignored):"; git status --porcelain --ignored=matching | head -20; echo "(end)"
echo "index-vs-HEAD: $(git diff --cached --quiet && echo clean || echo DIRTY)"
echo "worktree-vs-index: $(git diff --quiet && echo clean || echo DIRTY)"
git update-index --really-refresh >/dev/null 2>&1; echo "refresh-after: $(git diff --quiet && echo clean || echo DIRTY)"
echo "index tree: $(git write-tree)"
echo "gitlinks at HEAD:"; git ls-tree HEAD external gptp-processor protocol-processor third_party/verilog-axis
echo "submodule status:"; git submodule status
