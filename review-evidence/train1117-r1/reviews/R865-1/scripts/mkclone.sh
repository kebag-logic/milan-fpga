#!/bin/bash
# Make a disposable clone of the reviewed head with its submodules, from local objects only.
# usage: mkclone.sh <source clone> <dest dir> <sha>
set -euo pipefail
src=$1; dst=$2; sha=$3
git clone -q --shared --no-checkout "$src" "$dst"
git -C "$dst" checkout -q --detach "$sha"
for s in protocol-processor gptp-processor third_party/tsn-c-stack third_party/lwSRP third_party/verilog-axis; do
  link=$(git -C "$dst" ls-files -s "$s" | awk '{print $2}')
  rm -rf "$dst/$s"
  git clone -q --shared --no-checkout "$src/$s" "$dst/$s"
  git -C "$dst/$s" checkout -q --detach "$link"
done
echo "$dst $(git -C "$dst" rev-parse HEAD)"
