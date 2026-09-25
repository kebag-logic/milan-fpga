#!/usr/bin/env bash
# Copy the exact-head working tree (tracked files and checked-out submodules,
# no .git) into a disposable scratch tree, then prove the parent's tracked
# files in the copy equal the head blobs.
set -eu
REPO=${REPO:-$REVIEWS/r301-2-545}
PKT=${PKT:-$REVIEWS/545-r301-2-packet}
HEAD=b94f53cc4e5dbfd9527ba666922a55804515165c
T="$PKT/scratch/tree"
[ "$(git -C "$REPO" rev-parse HEAD)" = "$HEAD" ] || { echo "clone not at head"; exit 2; }
rm -rf "$T"; mkdir -p "$T"
rsync -a --exclude=.git "$REPO/" "$T/"
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; blob=$3
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  [ "$(git hash-object --no-filters -- "$T/$path")" = "$blob" ] || { bad=$((bad+1)); echo "DIFF $path"; }
done < <(git -C "$REPO" ls-tree -r "$HEAD")
echo "tree copy: $n tracked parent blobs compared, $bad differ"
for s in gptp-processor protocol-processor third_party/verilog-axis; do
  echo "$s gitlink $(git -C "$REPO" rev-parse "$HEAD:$s") checkout $(git -C "$REPO/$s" rev-parse HEAD)"
done
[ $bad -eq 0 ]
