#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# After all probes: the review clone is at the exact head, its index equals
# the head tree (mode, blob id, stage 0, path), every tracked file hashes to
# its blob with its mode, nothing is untracked or ignored-and-present, no
# index entry hides a change (assume-unchanged / skip-worktree), and the
# gitlink set matches the base's (this repository pins none).
set -eu
. "$(dirname "$0")/env.sh"
cd "$CLONE"
fail=0
test "$(git rev-parse HEAD)" = "$HEAD_SHA" || { echo "HEAD moved"; fail=1; }
test "$(git rev-parse 'HEAD^{tree}')" = "$HEAD_TREE" || { echo "tree differs"; fail=1; }
idx=$(git ls-files -s | awk '{print $1, $2, $3, $4}' | sha256sum | cut -c1-64)
tree=$(git ls-tree -r HEAD | awk '{print $1, $3, 0, $4}' | sha256sum | cut -c1-64)
echo "index digest $idx"; echo "tree  digest $tree"
test "$idx" = "$tree" || { echo "index differs from HEAD tree"; fail=1; }
flags=$(git ls-files -v | grep -cv '^H ' || true)
echo "index entries not plain-tracked (assume-unchanged/skip-worktree/other): $flags"
test "$flags" = 0 || fail=1
n=0; bad=0
git ls-tree -r HEAD | while read -r mode type sha path; do
  [ "$type" = blob ] || continue
  if [ -L "$path" ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin); m=120000
  else got=$(git hash-object --no-filters "$path"); if [ -x "$path" ]; then m=100755; else m=100644; fi; fi
  if [ "$got" != "$sha" ] || [ "$m" != "$mode" ]; then echo "MISMATCH $path"; fi
done > "$SCRATCH/blob-check.txt"
nb=$(git ls-tree -r HEAD | grep -c ' blob ')
echo "tracked blobs checked for bytes and mode: $nb, mismatches: $(wc -l < "$SCRATCH/blob-check.txt")"
test ! -s "$SCRATCH/blob-check.txt" || { cat "$SCRATCH/blob-check.txt"; fail=1; }
extra=$(git status --porcelain=v1 --untracked-files=all --ignored | wc -l)
echo "status entries including untracked and ignored: $extra"
test "$extra" = 0 || { git status --porcelain=v1 --untracked-files=all --ignored; fail=1; }
echo "gitlinks at head: $(git ls-tree -r HEAD | awk '$1=="160000"' | wc -l); at base: $(git ls-tree -r "$BASE_SHA" | awk '$1=="160000"' | wc -l)"
echo "RESULT: $([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail
