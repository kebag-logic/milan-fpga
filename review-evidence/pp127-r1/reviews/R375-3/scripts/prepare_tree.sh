#!/bin/sh
# Extract the exact head into the packet scratch area twice:
#   scratch/head       build parallelism capped at 2 per simulator build (the only
#                      edit; used for the partitioned campaign re-run)
#   scratch/head-pure  byte-identical git archive (used to exercise the committed
#                      `make -C tb/srp_top mutants` target unmodified)
# usage: prepare_tree.sh <path-to-processor-clone>
set -eu
PKT=$(cd "$(dirname "$0")/.." && pwd)
CLONE=$1
REV=0404675dcd8788d29cb15a831a8c182438bf1c92
for name in head head-pure; do
  rm -rf "$PKT/scratch/$name"; mkdir -p "$PKT/scratch/$name"
  git -C "$CLONE" archive "$REV" | tar -x -C "$PKT/scratch/$name"
done
for mk in "$PKT/scratch/head"/tb/*/Makefile; do
  sed -i 's/--build -j 0/--build -j 2/' "$mk"
done
