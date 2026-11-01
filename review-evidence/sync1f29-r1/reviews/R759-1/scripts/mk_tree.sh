#!/bin/sh
# Materialise a full tree of commit $2 of the review clone $1 at path $3: a shared clone with shared clones of the pinned submodules.
set -eu
clone=$1; sha=$2; dst=$3
git clone -q --shared --no-checkout "$clone" "$dst"
git -C "$dst" checkout -q "$sha"
for s in third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP; do
  pin=$(git -C "$dst" rev-parse "$sha:$s")
  rmdir "$dst/$s"
  git clone -q --shared --no-checkout "$clone/$s" "$dst/$s"
  git -C "$dst/$s" checkout -q "$pin"
done
