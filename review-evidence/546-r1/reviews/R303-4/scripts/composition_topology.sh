#!/usr/bin/env bash
# Composition topology receipt for the issue 546 merge-train candidate.
# Usage: composition_topology.sh <candidate-clone>
# Prints: parents, clean-merge tree identity, the overlap between what the
# 546 side adds and what the predecessor train changes relative to live dev,
# per-overlap-file blob identities, patch equivalence, and gitlinks.
set -u
cd "$1" || exit 2
CAND=59e7f5fd76786faa673b4522018f4e9590d294d0
TRAIN=2ab66c9de3a63942c4d3251e1354e8ad3a50d88c   # first parent: queued predecessors
SRC=f5532c4c3f94a516b748cc4627dc5f78d05fa73e     # second parent: PR #554 head
DEV=c266432dcb0cdd464205823a3d82cad260eedde2     # live dev
echo "candidate $(git rev-parse $CAND) tree $(git rev-parse $CAND^{tree})"
echo "parents: $(git rev-parse $CAND^1) $(git rev-parse $CAND^2)"
echo "clean merge-tree of parents: $(git merge-tree --write-tree $TRAIN $SRC | head -1)"
echo "dev ancestor of source: $(git merge-base --is-ancestor $DEV $SRC && echo yes || echo no)"
echo "dev ancestor of train: $(git merge-base --is-ancestor $DEV $TRAIN && echo yes || echo no)"
echo "commits in dev not in train (merge commits only expected):"
git rev-list --oneline $TRAIN..$DEV
echo "tree diff dev..train (content the predecessors add):"
git diff --stat $DEV $TRAIN | tail -1
echo "predecessor commits (train not in dev):"
git rev-list --oneline --no-merges $DEV..$TRAIN
echo "== files the 546 side adds on the train (train..candidate)"
git diff --name-only $TRAIN $CAND | sort | tee /tmp/r303_add.$$
echo "== files the predecessors change relative to dev (dev..train)"
git diff --name-only $DEV $TRAIN | sort | tee /tmp/r303_pred.$$
echo "== OVERLAP"
comm -12 /tmp/r303_add.$$ /tmp/r303_pred.$$
echo "== overlap blob table: path dev train source candidate"
for f in $(comm -12 /tmp/r303_add.$$ /tmp/r303_pred.$$); do
  printf '%s' "$f"
  for r in $DEV $TRAIN $SRC $CAND; do printf ' %s' "$(git rev-parse --short=12 $r:$f)"; done
  echo
done
echo "== owners of the overlap on the predecessor side"
for f in $(comm -12 /tmp/r303_add.$$ /tmp/r303_pred.$$); do
  git rev-list --oneline --no-merges $DEV..$TRAIN -- "$f" | sed "s|^|$f: |"
done
rm -f /tmp/r303_add.$$ /tmp/r303_pred.$$
echo "== patch equivalence: diff(train..candidate) vs diff(dev..source), header lines only expected"
diff <(git diff $TRAIN $CAND) <(git diff $DEV $SRC)
echo "rc=$?"
echo "== source-only suite paths identical source vs candidate"
git diff --stat $SRC $CAND -- hdl/ieee1722/crf tb/verilator/crf_rx tb/verilator/mmcm_servo tb/verilator/mmcm_servo_autorepair | tail -1
echo "(empty line above = byte-identical)"
echo "== gitlinks"
for r in $TRAIN $SRC $CAND; do git ls-tree $r external gptp-processor protocol-processor third_party/verilog-axis | sed "s|^|$r |"; done
