#!/bin/sh
# Compare the comment-stripped preprocessed output of the RTL files changed between two revisions.
# Usage: pp_identity.sh <repo> <old-rev> <new-rev> <workdir>   (VERILATOR = the pinned 5.050 wrapper)
R=$1; A=$2; B=$3; W=$4; V=${VERILATOR:-verilator}
mkdir -p "$W/old" "$W/new"
git -C "$R" archive "$A" hdl | tar -x -C "$W/old"
git -C "$R" archive "$B" hdl | tar -x -C "$W/new"
for f in $(git -C "$R" diff --name-only "$A" "$B" -- 'hdl/*.sv'); do
  for side in old new; do
    (cd "$W/$side" && $V -E -P $(find hdl -type d -printf '-I%p ') "$f" > "../$side.$(basename "$f").E")
  done
  if cmp -s "$W/old.$(basename "$f").E" "$W/new.$(basename "$f").E"; then echo "IDENTICAL $f"; else echo "DIFFERS $f"; fi
done
