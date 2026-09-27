#!/usr/bin/env bash
# For every path the PR delta (PR merge-base-with-dev .. PR head) changes, compare
# the candidate blob to the PR-head blob; for divergent paths, show the residual
# diff and the train's own delta for that path. Usage: check_blob_fidelity.sh <clone>
set -u; cd "$1" || exit 2
CAND=e79f23347f754f99d8312c19995431557c896404; PRH=7a051e618677ecd907ed04b086afbdfe374b4336
PRB=6d5ebd7357c1e468e446f18a61527c5be6118a04; TRAIN=1304205cfc9fa4c9e69a32130fb366895c5f883b
for f in $(git diff --name-only $PRB $PRH); do
  c=$(git ls-tree $CAND -- "$f"); p=$(git ls-tree $PRH -- "$f")
  if [ "$c" = "$p" ]; then echo "SAME-AS-PR-HEAD $c"; else echo "DIFFERS $f"; echo "  cand: $c"; echo "  prh : $p"; fi
done
echo "== residual candidate vs PR head (all paths the PR changed)"
git diff --no-ext-diff $PRH $CAND -- $(git diff --name-only $PRB $PRH)
echo "== train's own delta on those paths since PR base"
git diff --no-ext-diff $PRB $TRAIN -- $(git diff --name-only $PRB $PRH)
