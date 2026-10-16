#!/usr/bin/env bash
# Prove a two-parent merge adds no change of its own.
# Usage: merge_identity.sh <merge> (run inside a clone that has the merge and its parents)
set -euo pipefail
M=${1:?merge commit}
P1=$(git rev-parse "$M^1"); P2=$(git rev-parse "$M^2"); B=$(git merge-base "$P1" "$P2")
echo "merge $M parents $P1 $P2 base $B"
echo "head tree   $(git rev-parse "$M^{tree}")"
echo "replay tree $(git merge-tree --write-tree "$P1" "$P2")"
# file sets: M vs one parent == base vs the other parent
diff <(git diff --name-only "$P1" "$M") <(git diff --name-only "$B" "$P2") && echo "P1..M file set == base..P2"
diff <(git diff --name-only "$P2" "$M") <(git diff --name-only "$B" "$P1") && echo "P2..M file set == base..P1"
# files both sides touched: each side's patch reappears unchanged on the other parent
for f in $(comm -12 <(git diff --name-only "$B" "$P1" | sort) <(git diff --name-only "$B" "$P2" | sort)); do
  for pair in "$P2:$P1" "$P1:$P2"; do
    side=${pair%%:*}; other=${pair#*:}
    a=$(git diff "$B" "$side" -- "$f" | git patch-id --stable | cut -d' ' -f1)
    b=$(git diff "$other" "$M" -- "$f" | git patch-id --stable | cut -d' ' -f1)
    echo "$f side=${side:0:8} $a onto=${other:0:8} $b $([ "$a" = "$b" ] && echo EQUAL || echo DIFFERENT)"
  done
done
