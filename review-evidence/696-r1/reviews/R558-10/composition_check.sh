#!/bin/sh
# Composition facts for the delta under review.
# Usage: composition_check.sh <repo> <head> <merge> <source-head> <dev> <lane-base>
cd "$1" || exit 2
H=$2; M=$3; SRC=$4; D=$5; B=$6
echo "== merge commit parents (expect source head, then dev)"
git log -1 --format='%H %P' "$M"
echo "== fresh merge-tree of source head and dev, against the merge commit's tree"
fresh=$(git merge-tree --write-tree "$SRC" "$D"); rc=$?
echo "merge-tree rc=$rc tree=$fresh"
echo "merge commit tree=$(git rev-parse "$M^{tree}")"
[ "$fresh" = "$(git rev-parse "$M^{tree}")" ] && echo "automatic merge reproduced: yes" || echo "automatic merge reproduced: NO"
echo "== merge-base of source head and dev: $(git merge-base "$SRC" "$D")"
echo "== commits after the merge (expect one, docs only)"
git log --format='%H %P %s' "$M..$H"
git diff --stat "$M" "$H"
echo "== files the head differs from dev in (the PR's footprint at this head)"
git diff --name-only "$D" "$H"
echo "== per PR file: dev change since lane base / source change since lane base / dev-to-merge change"
for f in $(git diff --name-only "$D" "$H"); do
  d=$(git diff --numstat "$B" "$D" -- "$f" | awk '{print "+"$1"/-"$2}')
  s=$(git diff --numstat "$B" "$SRC" -- "$f" | awk '{print "+"$1"/-"$2}')
  m=$(git diff --numstat "$D" "$M" -- "$f" | awk '{print "+"$1"/-"$2}')
  echo "$f dev:${d:-none} source:${s:-none} dev..merge:${m:-none}"
done
echo "== patch-id of each PR file: lane base..source head against dev..merge"
for f in $(git diff --name-only "$D" "$H"); do
  a=$(git diff "$B" "$SRC" -- "$f" | git patch-id --stable | cut -d' ' -f1)
  b=$(git diff "$D" "$M" -- "$f" | git patch-id --stable | cut -d' ' -f1)
  [ "$a" = "$b" ] && s=same || s=DIFFERENT
  echo "$f $s"
done
echo "== milan_datapath.sv: dev to head (expect only the PR's two hunks)"
git diff "$D" "$H" -- hdl/milan/milan_datapath.sv
