#!/usr/bin/env bash
# History and issue-delta identity for PR #512 at the corrected head. Read-only.
set -euo pipefail
R=$VALIDATION_STORAGE/reviews/r222-478-r2
cd "$R"
HEAD_C=1496558d82cf35fc98dda0e781b2a1be643c301a
FIX_C=2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7
OLD_C=d81a302760b84f32d2aa019643f57682bb6e052c
AUTH_C=099e191137dd2797407fb8345a452bcc7a965608
BASE_NOW=88e9276b2a220c716f64a843f7e1eb8f9265e896
BASE_OLD=ec34fcdee0ca9ffa63564a9af8ad70a3a618de29
BASE_AUTH=b17580b91deb11f3441dfc5d7f9fafe539d929b8
FILES=(docs/ENDSTATION_BUILDER.md sw/builder/endstation_builder.py sw/builder/test_builder.py)

echo "## commit objects"
for c in $HEAD_C $FIX_C $OLD_C $AUTH_C $BASE_NOW; do
  echo "$c tree=$(git rev-parse "$c^{tree}") parents=$(git rev-list --parents -n1 "$c" | cut -d' ' -f2-)"
  echo "  subject-lines=$(git log -1 --format=%B "$c" | sed '/^$/d' | wc -l) subject=$(git log -1 --format=%s "$c")"
done

echo "## merge-tree reproduction of the head (parents $FIX_C + $BASE_NOW)"
mt=$(git merge-tree --write-tree "$FIX_C" "$BASE_NOW")
echo "merge-tree=$mt head-tree=$(git rev-parse "$HEAD_C^{tree}") equal=$([ "$mt" = "$(git rev-parse "$HEAD_C^{tree}")" ] && echo yes || echo NO)"

echo "## ancestry"
git merge-base --is-ancestor "$BASE_NOW" "$HEAD_C" && echo "base $BASE_NOW is ancestor of head: yes"
git merge-base --is-ancestor "$OLD_C" "$HEAD_C" && echo "old head $OLD_C is ancestor of head: yes"
git merge-base --is-ancestor "$AUTH_C" "$HEAD_C" && echo "author $AUTH_C is ancestor of head: yes"
echo "merge-base(head, base_now)=$(git merge-base "$HEAD_C" "$BASE_NOW")"

echo "## changed paths per range"
for rng in "$BASE_AUTH..$AUTH_C" "$BASE_OLD..$OLD_C" "$OLD_C..$FIX_C" "$BASE_NOW..$HEAD_C" "$OLD_C..$HEAD_C" "$BASE_OLD..$BASE_NOW"; do
  echo "-- $rng"; git diff --name-status --no-renames "${rng%..*}" "${rng#*..}"
done

echo "## per-file blob ids"
for c in $BASE_AUTH $AUTH_C $BASE_OLD $OLD_C $FIX_C $BASE_NOW $HEAD_C; do
  printf '%s' "$c"
  for f in "${FILES[@]}"; do printf ' %s' "$(git rev-parse "$c:$f" | cut -c1-12)"; done
  echo
done

echo "## full-index patch sha256 of the issue delta"
p() { git diff --full-index --no-renames "$1" "$2" -- "${FILES[@]}" | sha256sum | cut -d' ' -f1; }
echo "author  $BASE_AUTH..$AUTH_C : $(p $BASE_AUTH $AUTH_C)"
echo "round-1 $BASE_OLD..$OLD_C   : $(p $BASE_OLD $OLD_C)"
echo "head    $BASE_NOW..$HEAD_C  : $(p $BASE_NOW $HEAD_C)"
echo "## code-only (builder + test) patch sha256 (excludes the doc row)"
q() { git diff --full-index --no-renames "$1" "$2" -- sw/builder/endstation_builder.py sw/builder/test_builder.py | sha256sum | cut -d' ' -f1; }
echo "author  : $(q $BASE_AUTH $AUTH_C)"
echo "round-1 : $(q $BASE_OLD $OLD_C)"
echo "head    : $(q $BASE_NOW $HEAD_C)"
echo "## doc delta relative to round-1 head: only the link target differs"
git diff --word-diff=porcelain "$OLD_C" "$HEAD_C" -- docs/ENDSTATION_BUILDER.md | grep -E '^[-+][^-+]' || true

echo "## gitlinks: base_now vs head vs old head"
for c in $BASE_NOW $OLD_C $HEAD_C; do
  echo "-- $c"; git ls-tree -r "$c" | awk '$1=="160000"'
done
echo "## .gitmodules identical base_now vs head: $(git diff --quiet $BASE_NOW $HEAD_C -- .gitmodules && echo yes || echo NO)"
git show "$HEAD_C:.gitmodules"
echo "## configs/ unchanged base_now..head: $(git diff --quiet $BASE_NOW $HEAD_C -- configs && echo yes || echo NO)"
echo "## tb/ hdl/ avdecc/ unchanged base_now..head: $(git diff --quiet $BASE_NOW $HEAD_C -- tb hdl avdecc && echo yes || echo NO)"
echo "## .github/ unchanged base_now..head: $(git diff --quiet $BASE_NOW $HEAD_C -- .github && echo yes || echo NO)"
echo "## trailers in branch-only commits (base_now..head)"
git log --format='%H %s%n%(trailers:only,unfold)' "$BASE_NOW..$HEAD_C"
