#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Prove the review clone is still the exact published head: HEAD, tree, a
# clean status, every index entry equal to HEAD's tree (path, mode, blob),
# every worktree file hashing to its blob, and the gitlink population.
set -euo pipefail
. "$(dirname "$0")/env.sh"
cd "$REVIEW_CLONE"
test "$(git rev-parse HEAD)" = "$HEAD_SHA"; echo "HEAD $HEAD_SHA"
echo "tree $(git rev-parse 'HEAD^{tree}')"
test "$(git rev-parse 'HEAD^{tree}')" = 10154fc3f95ccc542a6f5dcd8a58105d302fd1af
test -z "$(git status --porcelain=v1 --untracked-files=all)"; echo "status: clean (no untracked files)"
diff <(git ls-files -s | awk '{print $1, $2, $4}') \
     <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') && echo "index == HEAD tree (mode, blob, path) for $(git ls-files | wc -l) entries"
bad=0
while IFS= read -r -d '' f; do
  want="$(git ls-tree HEAD -- "$f" | awk '{print $3}')"
  got="$(git hash-object --no-filters -- "$f")"
  [ "$want" = "$got" ] || { echo "BYTES DIFFER: $f"; bad=1; }
  mode="$(git ls-tree HEAD -- "$f" | awk '{print $1}')"
  if [ -x "$f" ]; then [ "$mode" = 100755 ] || { echo "MODE: $f"; bad=1; }
  else [ "$mode" = 100644 ] || { echo "MODE: $f"; bad=1; }; fi
done < <(git ls-files -z)
[ $bad = 0 ] && echo "worktree bytes and executable bits == HEAD blobs"
echo "gitlinks (mode 160000): $(git ls-tree -r HEAD | awk '$1=="160000"' | wc -l) (the donor pins none)"
echo "ignored build outputs present: $(git status --porcelain --ignored | grep -c '^!!' || true)"
exit $bad
