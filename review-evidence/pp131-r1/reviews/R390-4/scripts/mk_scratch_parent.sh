#!/bin/sh
# Build a disposable scratch parent (no git metadata) from a parent clone at a
# revision, with protocol-processor from the review clone at a revision and
# gptp-processor from its source clone at the parent's gitlink.
# Usage: mk_scratch_parent.sh <dest> <parent-clone> <parent-rev> <pp-clone> <pp-rev> <gptp-clone>
set -eu
D=$1; PC=$2; PR=$3; PPC=$4; PPR=$5; GC=$6
rm -rf "$D"; mkdir -p "$D"
git -C "$PC" archive "$PR" | tar -x -C "$D"
GL=$(git -C "$PC" ls-tree "$PR" gptp-processor | awk '{print $3}')
rm -rf "$D/protocol-processor" "$D/gptp-processor"
mkdir -p "$D/protocol-processor" "$D/gptp-processor"
git -C "$PPC" archive "$PPR" | tar -x -C "$D/protocol-processor"
git -C "$GC" archive "$GL" | tar -x -C "$D/gptp-processor"
echo "scratch parent $PR, protocol-processor $PPR, gptp-processor $GL"
