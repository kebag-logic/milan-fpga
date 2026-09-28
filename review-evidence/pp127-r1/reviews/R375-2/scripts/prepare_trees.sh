#!/bin/sh
# Extract the exact head, the round-1 head and the base into the packet
# scratch area, and cap each extraction's simulator build parallelism at 2
# (build flag only; sources are otherwise byte-identical to git archive).
# usage: prepare_trees.sh <path-to-processor-clone>
set -eu
PKT=$(cd "$(dirname "$0")/.." && pwd)
CLONE=$1
for pair in head:00b5c6c96af5ebcaa92ddb3bdaeb4aa5302ef27c \
            r1:cf4e5c63ab12442c6c63d2bfe2bb64902674d55e \
            base:16be6768f710e79450aace277abacd6c2c3336e5; do
  name=${pair%%:*}; rev=${pair#*:}
  rm -rf "$PKT/scratch/$name"; mkdir -p "$PKT/scratch/$name"
  git -C "$CLONE" archive "$rev" | tar -x -C "$PKT/scratch/$name"
  for mk in "$PKT/scratch/$name"/tb/*/Makefile; do
    sed -i 's/--build -j 0/--build -j 2/' "$mk"
  done
done
# Simulator: prepend the pinned 5.050 wrapper directory to PATH, e.g.
#   PATH=$VALIDATION_STORAGE/pp127-manager-00b5c6c9/pinned-tool-bin:$PATH
