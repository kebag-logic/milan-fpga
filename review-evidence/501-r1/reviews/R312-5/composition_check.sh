#!/usr/bin/env bash
# Structural composition receipts for the issue 501 merge-train candidate.
# Usage: composition_check.sh <clone>   (read-only: no ref, index or worktree write)
set -u
cd "$1" || exit 2
CAND=2ab66c9de3a63942c4d3251e1354e8ad3a50d88c
PARENT=0b81fdc969131b82c535c4a183a78065fd1cd2d8   # queued predecessors (dev 408 step, 387b, 548)
PR=efcabc379b1e0be1366bfc05bdcc05a759b55616       # reviewed source head
DEV=ffcbd33de70278ae34b533dcbadde0b36c8cba13      # live dev tip
bad=0
echo "candidate parents: $(git rev-list --parents -n1 $CAND)"
mb=$(git merge-base $PARENT $PR); echo "merge base (PR source base): $mb"
t=$(git merge-tree --write-tree $PARENT $PR) && [ "$t" = "$(git rev-parse $CAND^{tree})" ] \
  && echo "clean merge-tree of parent+PR == candidate tree $t" || { echo "MERGE TREE MISMATCH/CONFLICT: $t"; bad=1; }
# the candidate's dev step is tree-identical to live dev
step=$(git rev-list --first-parent $PARENT | while read c; do [ "$(git log -1 --format=%s $c)" = "Validate issue 408 merge-train candidate" ] && echo $c && break; done)
[ "$(git rev-parse $step^{tree})" = "$(git rev-parse $DEV^{tree})" ] \
  && echo "408 step $step tree == live dev $DEV tree" || { echo "DEV TREE MISMATCH"; bad=1; }
git diff --name-only $mb $PR | sort > /tmp/c501_pr.txt
git diff --name-only $mb $PARENT | sort > /tmp/c501_pred.txt
git diff --name-only $PARENT $CAND | sort > /tmp/c501_c1.txt
git diff --name-only $PR $CAND | sort > /tmp/c501_c2.txt
cmp -s /tmp/c501_pr.txt /tmp/c501_c1.txt && echo "files(parent..candidate) == files(PR source) ($(wc -l </tmp/c501_pr.txt))" || { echo "PR FILESET DIFFERS"; bad=1; }
cmp -s /tmp/c501_pred.txt /tmp/c501_c2.txt && echo "files(PR..candidate) == files(predecessors) ($(wc -l </tmp/c501_pred.txt))" || { echo "PRED FILESET DIFFERS"; bad=1; }
echo "overlap (changed by both):"; comm -12 /tmp/c501_pr.txt /tmp/c501_pred.txt | sed 's/^/  /'
for step in "$mb 44873590 dev408" "44873590 e1333a14 387b" "e1333a14 $PARENT 548"; do
  set -- $step; echo "  $3 touches: $(git diff --name-only $1 $2 | grep -xF -f <(comm -12 /tmp/c501_pr.txt /tmp/c501_pred.txt) | tr '\n' ' ')"
done
# per overlap file: the PR's own hunks apply unchanged onto the predecessor side
for f in $(comm -12 /tmp/c501_pr.txt /tmp/c501_pred.txt); do
  a=$(git diff $mb $PR -- "$f" | git patch-id --stable | cut -d' ' -f1)
  b=$(git diff $PARENT $CAND -- "$f" | git patch-id --stable | cut -d' ' -f1)
  [ "$a" = "$b" ] && echo "  $f: PR delta patch-id $a identical on predecessor side" || { echo "  $f: PR DELTA CHANGED BY MERGE ($a vs $b)"; bad=1; }
done
# predecessor RTL does not reach the output-map key space or the NVM RTL/pins
for r in $mb $CAND; do printf '%s amap_edit_validate sha256 %s\n' "${r:0:8}" \
  "$(git show $r:hdl/milan/milan_datapath.sv | awk '/always_comb begin : amap_edit_validate/,/end : amap_edit_validate/' | sha256sum | cut -c1-16)"; done
for p in hdl/milan/KL_nvm_backend.sv protocol-processor gptp-processor third_party/verilog-axis; do
  [ "$(git rev-parse $mb:$p)" = "$(git rev-parse $CAND:$p)" ] && echo "unchanged base..candidate: $p $(git rev-parse $CAND:$p)" || { echo "CHANGED: $p"; bad=1; }
done
exit $bad
