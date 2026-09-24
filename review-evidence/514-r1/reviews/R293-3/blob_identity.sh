#!/usr/bin/env bash
# [R293] R293-3: prove the candidate is the plain composition of its two parents.
# Usage: blob_identity.sh <repo>   (prints the receipt on stdout)
set -u
export LC_ALL=C
cd "$1" || exit 2
BASE=3d2f3e3131c9db5898e1db9dd3e2a35149843109   # PR source fork point on dev
PARENT=cf43b4716772582d0c77d40f1eeac5934a0cd9da # predecessor merge-train tip
SRC=b0347a4fd668f8d40bdf40a142ac0ea70167acd1    # PR source head
CAND=177867daf3b35ba41b8c51f8c35c8509643dda22   # candidate
oid() { git rev-parse --verify -q "$1:$2" || echo absent; }
echo "merge-base(PARENT,SRC)=$(git merge-base $PARENT $SRC)"
echo "candidate parents: $(git rev-parse $CAND^1 $CAND^2 | tr '\n' ' ')"
echo "candidate tree=$(git rev-parse $CAND^{tree}) mechanical merge-tree=$(git merge-tree --write-tree $PARENT $SRC)"
git diff --name-only $BASE $PARENT | sort > /tmp/r293-pred.$$
git diff --name-only $BASE $SRC | sort > /tmp/r293-pr.$$
echo "# PR-changed paths: source head vs candidate"
while read -r p; do a=$(oid $SRC "$p"); b=$(oid $CAND "$p")
  [ "$a" = "$b" ] && s=IDENTICAL || s=DIFFERS; echo "$s $p $a $b"; done < /tmp/r293-pr.$$
echo "# predecessor-only paths: parent vs candidate"
comm -23 /tmp/r293-pred.$$ /tmp/r293-pr.$$ | while read -r p; do a=$(oid $PARENT "$p"); b=$(oid $CAND "$p")
  [ "$a" = "$b" ] && s=IDENTICAL || s=DIFFERS; echo "$s $p $a $b"; done
echo "# overlapping paths (changed on both sides since $BASE)"
comm -12 /tmp/r293-pred.$$ /tmp/r293-pr.$$
echo "# overlapping paths: PR hunk bodies (base->src) vs composed hunk bodies (parent->cand)"
comm -12 /tmp/r293-pred.$$ /tmp/r293-pr.$$ | while read -r p; do
  if cmp -s <(git diff -U0 $BASE $SRC -- "$p" | grep -v '^@@\|^index ') \
            <(git diff -U0 $PARENT $CAND -- "$p" | grep -v '^@@\|^index '); then
    echo "SAME-HUNKS $p"; else echo "HUNKS-DIFFER $p"; fi; done
echo "# candidate-vs-parent paths outside the PR set"
git diff --name-only $PARENT $CAND | sort | comm -23 - /tmp/r293-pr.$$ | sed 's/^/EXTRA /'
echo "# gitlinks at candidate"
git ls-tree $CAND | awk '$2=="commit"'
rm -f /tmp/r293-pred.$$ /tmp/r293-pr.$$
echo "# end"
