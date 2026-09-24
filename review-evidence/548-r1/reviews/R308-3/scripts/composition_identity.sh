#!/bin/sh
# Prove the candidate is exactly the clean merge of the predecessor candidate
# and the reviewed source head, and name every file both sides changed.
# Usage: composition_identity.sh <repo>
set -u
cd "$1"
head=0b81fdc969131b82c535c4a183a78065fd1cd2d8
parent=e1333a144115f074f8e3bdcd1de2d3a29d7f9dfd
src=8544472a19a4b4d3853d64b15dea22f999372a32
echo "git $(git --version)"
echo "head $(git rev-parse $head) tree $(git rev-parse "$head^{tree}")"
echo "head parents: $(git rev-parse "$head^1") $(git rev-parse "$head^2")"
mb=$(git merge-base $parent $src)
echo "merge-base(parent, src) $mb"
echo "recomputed merge tree $(git merge-tree --write-tree $parent $src)"
echo "== files the source changes (mb..src)"
git diff --name-only "$mb" $src | sort > /tmp/r308_src_files.$$
cat /tmp/r308_src_files.$$
echo "== files the predecessor side changes (mb..parent) that the source also changes"
git diff --name-only "$mb" $parent | sort | comm -12 - /tmp/r308_src_files.$$
rm -f /tmp/r308_src_files.$$
echo "== per-file patch identity: source (mb..src) vs composition (parent..head)"
for f in $(git diff --name-only $parent $head); do
  a=$(git diff "$mb" $src -- "$f" | git patch-id --stable | cut -d' ' -f1)
  b=$(git diff $parent $head -- "$f" | git patch-id --stable | cut -d' ' -f1)
  [ "$a" = "$b" ] && v=SAME || v=DIFF
  echo "$v $f $a $b"
done
echo "== whole-patch identity"
echo "source      $(git diff "$mb" $src | git patch-id --stable | cut -d' ' -f1)"
echo "composition $(git diff $parent $head | git patch-id --stable | cut -d' ' -f1)"
echo "predecessor side (mb..parent) $(git diff "$mb" $parent | git patch-id --stable | cut -d' ' -f1)"
echo "other side    (src..head)     $(git diff $src $head | git patch-id --stable | cut -d' ' -f1)"
echo "== gitlinks parent/src/head"
for c in $parent $src $head; do git ls-tree -r $c | awk -v c=$c '$2=="commit"{print substr(c,1,8), $3, $4}'; done
echo "== composition diffstat"
git diff --stat $parent $head
