#!/bin/bash
# Usage: composition_checks.sh <clone> <receipt-dir>
# Reproduces the git-level composition evidence for the #551 merge-train
# candidate: overlap inventory, independent re-merge, per-file blob and hunk
# equality, CHANGELOG entry survival and the stale-wording searches.
set -u
C=$1; OUT=$2
CAND=0e26e0ac07abf1043ac2712fe39f92de0b34f2dd
PRED=d47a04ebf2a5193dd06ed4eecf8be00f5c8502ce   # C_559: #559 on #443 on dev lineage
SRC=6e4a3b420e055ef7529ceb16bb2ab5be93c34487    # PR #553 source head
MB=864b36f5e9450ef64f75ca3f0d68c44330e447d7     # PR merge-base with the candidate
DEV=fd9e0ebf2bbaa38330e99d1c489f01a820f1c363    # live dev
C443=4ee96a61bf35402a6f88e1ebad1167e9873721c5
cd "$C" || exit 2
{
echo "# dev tree == #541 candidate tree (ec9cf454):"
echo "  $(git rev-parse $DEV^{tree}) $(git rev-parse ec9cf454^{tree})"
git diff --name-only $MB $SRC | sort > "$OUT/files_pr551.txt"
git diff --name-only $MB $PRED | sort > "$OUT/files_predecessors_since_mb.txt"
git diff --name-only $MB $DEV | sort > "$OUT/files_dev562.txt"
git diff --name-only $DEV $C443 | sort > "$OUT/files_443.txt"
git diff --name-only $C443 $PRED | sort > "$OUT/files_559.txt"
comm -12 "$OUT/files_pr551.txt" "$OUT/files_predecessors_since_mb.txt" > "$OUT/files_overlap.txt"
echo "# overlap:"; sed 's/^/  /' "$OUT/files_overlap.txt"
echo "# independent re-merge of $PRED and $SRC:"
echo "  merge-tree $(git merge-tree --write-tree $PRED $SRC | head -1) candidate $(git rev-parse $CAND^{tree})"
echo "# non-overlap PR files: candidate blob == source blob"
for f in $(comm -23 "$OUT/files_pr551.txt" "$OUT/files_overlap.txt"); do
  [ "$(git rev-parse $CAND:$f)" = "$(git rev-parse $SRC:$f)" ] && echo "  SAME $f" || echo "  DIFF $f"
done
echo "# overlap files: #551 +/- lines identical in source and composition"
for f in $(cat "$OUT/files_overlap.txt"); do
  a=$(git diff --no-color --no-ext-diff $MB $SRC -- "$f" | grep '^[-+]' | grep -v '^[-+][-+][-+]' | sha256sum | cut -c1-16)
  b=$(git diff --no-color --no-ext-diff $PRED $CAND -- "$f" | grep '^[-+]' | grep -v '^[-+][-+][-+]' | sha256sum | cut -c1-16)
  [ "$a" = "$b" ] && echo "  SAME $f" || echo "  DIFF $f"
done
echo "# CHANGELOG: lines of $PRED missing from candidate == lines #551 removed"
diff <(comm -23 <(git show $PRED:CHANGELOG.md | sort -u) <(git show $CAND:CHANGELOG.md | sort -u)) \
     <(comm -23 <(git show $MB:CHANGELOG.md | sort -u) <(git show $SRC:CHANGELOG.md | sort -u)) \
  && echo "  IDENTICAL"
echo "# predecessor hunks touching licence/grant terms (expect none)"
git diff --no-color --no-ext-diff $DEV $PRED | grep -E '^[-+]' \
  | grep -E "LWSRP_STATUS|CRFT_CTRL|ACTIVE\b|real grant|licen[cs]e|lwsrp_stream_gate|sr_admitted" || echo "  none"
echo "# stale wording searches at candidate (expect none)"
git grep -nE "Residual|pending fix|previous slope" $CAND -- tests/ || echo "  none (tests/)"
git grep -niE "whether the licence should also need|Issue #551 asks" $CAND || echo "  none (tree)"
} > "$OUT/composition_checks.txt" 2>&1
cat "$OUT/composition_checks.txt"
