#!/usr/bin/env bash
# Composition facts for the #730 merge-train candidate. Read-only on the repo.
# Usage: composition_facts.sh <candidate-checkout>
set -u
cd "$1" || exit 2
CAND=ac0142539856222b84ef8e5af414d12132a5bebf
PR=b341e875d87c6aa2be355bad17f373782517f723
BASE=dc4d06cbfec209cc2ff76806f4b49c51f46639ae
TRAIN=ada26e56ac42ee5de311aef84cb86c8435b97cee
DEV=49da9fd974e8805d56c90e29dcfcb67994c2c430
g() { git "$@" 2>/dev/null; }
echo "HEAD=$(g rev-parse HEAD) tree=$(g rev-parse HEAD^{tree}) expected=$CAND"
echo "parents: $(g rev-parse $CAND^1) $(g rev-parse $CAND^2)"
echo "merge-base(PR,train)=$(g merge-base $PR $TRAIN)"
echo "recomputed merge-tree(train,PR)=$(g merge-tree --write-tree $TRAIN $PR)"
echo "recomputed merge-tree(dev,PR)=$(g merge-tree --write-tree $DEV $PR)"
echo; echo "== files the PR changes ($BASE..$PR)"; g diff --name-only $BASE $PR | tee /tmp/r632_pr.$$
echo; echo "== files the train delta changes ($BASE..$TRAIN): $(g diff --name-only $BASE $TRAIN | wc -l)"
g diff --name-only $BASE $TRAIN > /tmp/r632_tr.$$
echo "== overlap"; comm -12 <(sort /tmp/r632_pr.$$) <(sort /tmp/r632_tr.$$)
echo "== train-delta files under .github: $(grep -c '^\.github/' /tmp/r632_tr.$$)"
echo "== .github diff BASE..CAND (empty means no workflow change anywhere in the stack):"; g diff --stat $BASE $CAND -- .github
echo "== train commits touching the overlap"; g log --format='%h %s' $BASE..$TRAIN -- docs/testing/CI_WORKFLOWS.md
echo; echo "== blobs (base / train parent / PR head / candidate / merge(dev,PR))"
DT=$(g merge-tree --write-tree $DEV $PR)
for f in docs/testing/CI_WORKFLOWS.md scripts/act_ci.py .github/workflows/rtl.yml .github/workflows/docs.yml .github/workflows/elaborate.yml .github/workflows/rtl-fast.yml; do
  echo "$f: $(g rev-parse $BASE:$f) $(g rev-parse $TRAIN:$f) $(g rev-parse $PR:$f) $(g rev-parse $CAND:$f) $(g rev-parse $DT:$f)"
done
echo; echo "== max-parallel in workflows (none means act default 4 for matrix jobs):"; grep -n 'max-parallel' .github/workflows/*.yml || echo none
rm -f /tmp/r632_pr.$$ /tmp/r632_tr.$$
