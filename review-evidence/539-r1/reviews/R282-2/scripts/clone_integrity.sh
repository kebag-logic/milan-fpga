#!/bin/sh
# Verify the review clone is at the exact head with pristine tracked bytes,
# modes, index and submodule gitlinks.
set -u
. "$(dirname "$0")/env.sh"
cd "$CLONE"
echo "HEAD=$(git rev-parse HEAD) expect $HEAD_SHA"
echo "TREE=$(git rev-parse 'HEAD^{tree}') expect 9dac4c8295506c4600126e692531c02053fd971c"
echo "INDEX_TREE=$(git write-tree)"
echo "status-lines=$(git status --porcelain --ignore-submodules=none | wc -l)"
git diff --quiet HEAD && echo "worktree-vs-HEAD: identical" || echo "worktree-vs-HEAD: DIFFERS"
git diff --cached --quiet HEAD && echo "index-vs-HEAD: identical" || echo "index-vs-HEAD: DIFFERS"
echo "gitlinks at HEAD:"; git ls-tree HEAD external gptp-processor protocol-processor third_party/verilog-axis
echo "submodule status:"; git submodule status
