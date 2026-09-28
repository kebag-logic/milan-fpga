#!/bin/sh
# Extract one commit of the review clone into a scratch tree (git archive, read-only
# on the clone) and point its submodule paths at the clone's checked-out submodules.
# Prints the commit's gitlinks so the reuse is checked, not assumed.
# Usage: extract_tree.sh <clone> <commit> <dest>
set -eu
clone=$1; sha=$2; dest=$3
rm -rf "$dest"; mkdir -p "$dest"
git -C "$clone" archive "$sha" | tar -x -C "$dest"
for m in protocol-processor gptp-processor third_party/verilog-axis; do
  rmdir "$dest/$m" 2>/dev/null || true
  ln -s "$clone/$m" "$dest/$m"
done
git -C "$clone" ls-tree "$sha" protocol-processor gptp-processor third_party/verilog-axis
git -C "$clone/protocol-processor" rev-parse HEAD | sed 's/^/checked-out protocol-processor: /'
