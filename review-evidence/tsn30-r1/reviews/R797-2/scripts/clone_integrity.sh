#!/usr/bin/env bash
# Verify the review clone still holds the exact head bytes, modes and index.
# Usage: clone_integrity.sh <review-clone> <expected-head> <expected-tree>
set -u
C=$1; H=$2; T=$3
cd "$C" || exit 2
echo "head=$(git rev-parse HEAD) tree=$(git rev-parse HEAD^{tree}) expected=$H/$T"
[ "$(git rev-parse HEAD)" = "$H" ] && [ "$(git rev-parse HEAD^{tree})" = "$T" ] && echo "head-and-tree: exact" || echo "head-and-tree: MISMATCH"
echo "status-porcelain-lines=$(git status --porcelain --ignored | wc -l)"
diff <(git ls-files -s | awk '{print $1, $2, $4}') <(git ls-tree -r HEAD | awk '{print $1, $3, $4}') >/dev/null && echo "index-vs-head-tree: identical" || echo "index-vs-head-tree: DIFFER"
bad=0; while IFS= read -r -d '' f; do want=$(git rev-parse "HEAD:$f"); got=$(git hash-object --no-filters -- "$f"); [ "$want" = "$got" ] || { echo "blob mismatch: $f"; bad=1; }; done < <(git ls-files -z)
[ $bad = 0 ] && echo "worktree-blob-hashes: match"
echo "gitlinks-in-head=$(git ls-tree -r HEAD | awk '$1=="160000"' | wc -l) gitmodules=$([ -e .gitmodules ] && echo present || echo absent)"
for f in scripts/check_privacy.py CHANGELOG.md docs/IMPORT.md docs/VERIFICATION.md; do git ls-tree HEAD "$f" | awk -v f="$f" '{print f, "blob=" $3, "mode=" $1}'; done
