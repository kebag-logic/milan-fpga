#!/bin/sh
# Print the exact-head identity of a clone: HEAD, tree, index digest,
# status (tracked, untracked, ignored) and the submodule gitlinks.
set -eu
cd "$1"
echo "HEAD $(git rev-parse HEAD)"
echo "TREE $(git rev-parse 'HEAD^{tree}')"
echo "INDEX_TREE $(git write-tree)"
echo "INDEX_STAGE_SHA256 $(git ls-files -s | sha256sum | cut -d' ' -f1)"
echo "WORKTREE_DIFF_VS_HEAD $(git diff HEAD --name-only | wc -l)"
echo "STATUS_PORCELAIN:"
git status --porcelain=v1 --ignored --untracked-files=all | sed 's/^/  /' | head -50
echo "GITLINKS:"
git ls-tree HEAD protocol-processor gptp-processor third_party/verilog-axis external | sed 's/^/  /'
echo "SUBMODULE_HEADS:"
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  echo "  $s $(git -C "$s" rev-parse HEAD) dirty=$(git -C "$s" status --porcelain --ignored | wc -l)"
done
