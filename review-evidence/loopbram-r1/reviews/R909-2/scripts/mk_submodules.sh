#!/usr/bin/env bash
# Populate a scratch clone's submodules at their recorded gitlinks from a local
# source clone's module stores (shared, read-only use of the source).
# usage: mk_submodules.sh <source-clone> <scratch-clone>
set -euo pipefail
src=$1; dst=$2
for s in gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis; do
  pin=$(git -C "$dst" ls-files -s -- "$s" | awk '{print $2}')
  git clone -q --shared --no-checkout "$src/.git/modules/$s" "$dst/$s"
  git -C "$dst/$s" -c advice.detachedHead=false checkout -q "$pin"
  echo "$s $pin $(git -C "$dst/$s" rev-parse HEAD)"
done
