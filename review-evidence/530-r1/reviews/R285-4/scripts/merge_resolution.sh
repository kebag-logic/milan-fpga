#!/bin/sh
# Recompute the 3-way merge of each file both sides of merge 44ad6991 touched
# (base 50e78097, ours e65dccfe, theirs dev f86c34fe) with git merge-file, and
# show how the committed merge result differs from the automatic merge.
# A clean overlap must equal the automatic result; a conflicted one must keep
# both sides. Usage: merge_resolution.sh <repo> <scratch-dir>
set -eu
repo=$1
out=$2
base=50e78097564244c124e1ec30dd8821f83951ab06
ours=e65dccfe586bea9455cf1e10397d275c220c740a
theirs=f86c34fe2ddbc6cfb7c8c70ddbe0d9726f4d3c2f
merge=44ad6991fca85706343d1f2f84703ecf80d4da72
head=f814d37d94e17435f3b6dcc424f8b2b606cdd3e9
mkdir -p "$out"
echo "merge parents: $(git -C "$repo" log -1 --format=%P $merge)"
echo "merge base of parents: $(git -C "$repo" merge-base $ours $theirs)"
echo "files changed on both sides since the base:"
git -C "$repo" diff --name-only $base $ours | sort > "$out/ours.lst"
git -C "$repo" diff --name-only $base $theirs | sort > "$out/theirs.lst"
comm -12 "$out/ours.lst" "$out/theirs.lst" | tee "$out/both.lst"
echo "one-sided files not equal to their side at the merge (expect none):"
for f in $(comm -23 "$out/ours.lst" "$out/theirs.lst"); do
  git -C "$repo" show $ours:"$f" > "$out/a" 2>/dev/null || : > "$out/a"
  git -C "$repo" show $merge:"$f" > "$out/b" 2>/dev/null || : > "$out/b"
  cmp -s "$out/a" "$out/b" || echo "  DIFF $f"
done
for f in $(comm -13 "$out/ours.lst" "$out/theirs.lst"); do
  git -C "$repo" show $theirs:"$f" > "$out/a" 2>/dev/null || : > "$out/a"
  git -C "$repo" show $merge:"$f" > "$out/b" 2>/dev/null || : > "$out/b"
  cmp -s "$out/a" "$out/b" || echo "  DIFF $f"
done
echo "(end)"
for f in $(cat "$out/both.lst"); do
  case $f in *.png) echo "== $f: binary, judged by the diagram gates"; continue;; esac
  git -C "$repo" show $base:"$f" > "$out/base"
  git -C "$repo" show $ours:"$f" > "$out/ours"
  git -C "$repo" show $theirs:"$f" > "$out/theirs"
  git -C "$repo" show $merge:"$f" > "$out/merge"
  git -C "$repo" show $head:"$f" > "$out/head"
  rc=0
  git merge-file -p "$out/ours" "$out/base" "$out/theirs" > "$out/auto" || rc=$?
  same=no
  cmp -s "$out/merge" "$out/head" && same=yes
  echo "== $f: merge-file conflicts=$rc; merge result == head: $same"
  diff "$out/auto" "$out/merge" | cut -c1-240 || :
done
