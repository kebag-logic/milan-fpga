#!/usr/bin/env bash
# Verify the review clone is exactly the published head: HEAD, tree, index == tree
# (paths, modes, blob ids), every tracked working file re-hashes to its blob, no
# untracked/ignored residue, and the gitlink inventory (this repository has none).
set -uo pipefail
C=${CLONE:-$REVIEWS/r334-1-pp120}; HEAD=a9b7874d415d935949becd7ccfd58799927efb08
TREE=14040d6f4646d648748540d73c1c2e38de4f2b2e; cd "$C"; fail=0
[ "$(git rev-parse HEAD)" = "$HEAD" ] && echo "HEAD ok $HEAD" || { echo "HEAD MISMATCH"; fail=1; }
[ "$(git rev-parse HEAD^{tree})" = "$TREE" ] && echo "tree ok $TREE" || { echo "TREE MISMATCH"; fail=1; }
[ "$(git write-tree)" = "$TREE" ] && echo "index writes tree $TREE" || { echo "INDEX != TREE"; fail=1; }
a=$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sort | sha256sum)
b=$(git ls-files -s | awk '{print $1, $2, $4}' | sort | sha256sum)
[ "$a" = "$b" ] && echo "index modes/blobs == tree ($(git ls-files | wc -l) entries)" || { echo "INDEX MODE/BLOB DRIFT"; fail=1; }
bad=0
while IFS= read -r line; do
  mode=${line%% *}; rest=${line#* }; blob=${rest%% *}; path=${line#*$'\t'}
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin)
  else got=$(git hash-object --no-filters -- "$path"); fi
  [ "$got" = "$blob" ] || { echo "BLOB DRIFT $path"; bad=1; }
  if [ "$mode" = 100755 ] && [ ! -x "$path" ]; then echo "MODE DRIFT $path"; bad=1; fi
  if [ "$mode" = 100644 ] && [ -x "$path" ]; then echo "MODE DRIFT $path"; bad=1; fi
done < <(git ls-files -s)
[ $bad = 0 ] && echo "every tracked file re-hashes to its blob with its mode" || fail=1
st=$(git status --porcelain --ignored); [ -z "$st" ] && echo "no untracked/ignored residue" || { echo "RESIDUE:"; echo "$st"; fail=1; }
echo "gitlinks: $(git ls-files -s | awk '$1==160000' | wc -l) (none required in this repository)"
exit $fail
