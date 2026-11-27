#!/bin/sh
# Composition analysis of a merge-train candidate: run from the candidate checkout.
# Usage: composition.sh <candidate> <train-parent> <pr-head> <base>
set -eu
C=$1 T=$2 H=$3 B=$4
echo "candidate $(git rev-parse $C) tree $(git rev-parse $C^{tree}) parents $(git log -1 --format=%P $C)"
echo "merge-base(pr-head, train-parent) $(git merge-base $H $T) (expected base $B)"
echo "clean merge-tree of train-parent and pr-head: $(git merge-tree --write-tree $T $H)"
git diff --name-only $B $H | sort > /tmp/comp_pr.$$
git diff --name-only $B $T | sort > /tmp/comp_pred.$$
echo "PR files: $(wc -l < /tmp/comp_pr.$$); predecessor files: $(wc -l < /tmp/comp_pred.$$)"
echo "files changed by both:"; comm -12 /tmp/comp_pr.$$ /tmp/comp_pred.$$ | sed 's/^/  /'
echo "per-file hunk identity (PR diff on base vs candidate delta on train-parent):"
for f in $(cat /tmp/comp_pr.$$); do
  a=$(git diff $B $H -- "$f" | git patch-id --stable | cut -c1-40)
  b=$(git diff $T $C -- "$f" | git patch-id --stable | cut -c1-40)
  [ "$a" = "$b" ] && echo "  same $f" || echo "  DIFF $f"
done
echo "candidate delta outside PR files: $(git diff --name-only $T $C | sort | comm -23 - /tmp/comp_pr.$$ | wc -l)"
rm -f /tmp/comp_pr.$$ /tmp/comp_pred.$$
