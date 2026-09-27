#!/bin/sh
# Print the clone's tracked-state identity: head, tree, index digest, dirty paths, gitlinks.
cd "${1:?clone}" || exit 2
echo "head $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})"
echo "index-stage-sha256 $(git ls-files -s | sha256sum | cut -d' ' -f1)"
git update-index -q --refresh
echo "diff-vs-head-rc $(git diff --quiet HEAD; echo $?) cached-rc $(git diff --cached --quiet HEAD; echo $?)"
echo "untracked:"; git status --porcelain --untracked-files=all | sed 's/^/  /'
echo "gitlinks:"; git ls-files -s protocol-processor gptp-processor third_party/verilog-axis external | sed 's/^/  /'
echo "submodule status:"; git submodule status | sed 's/^/  /'
for s in protocol-processor gptp-processor third_party/verilog-axis; do
  echo "  $s dirty: $(git -C $s status --porcelain --untracked-files=all | wc -l)"
done
