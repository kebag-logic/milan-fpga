#!/bin/sh
# Export the exact head tree (and the three pinned submodules the focused
# suites read) into a disposable directory; the review clone is not built in.
# Usage: export_head.sh <clone-dir> <dest-dir> [rev]
set -eu
C=${1:?clone}; D=${2:?dest}; REV=${3:-HEAD}
rm -rf "$D"; mkdir -p "$D"
git -C "$C" archive --format=tar "$REV" | tar -x -C "$D"
for sm in third_party/verilog-axis protocol-processor gptp-processor; do
  pin=$(git -C "$C" rev-parse "$REV:$sm")
  mkdir -p "$D/$sm"
  git -C "$C/$sm" archive --format=tar "$pin" | tar -x -C "$D/$sm"
  echo "$sm pinned $pin exported"
done
echo "exported $(git -C "$C" rev-parse "$REV") tree $(git -C "$C" rev-parse "$REV^{tree}") to $D"
