#!/usr/bin/env bash
# Usage: make_clone.sh <source-clone> <dest> <commit>
# Local clone at <commit> with its submodules initialised from the source
# clone's own submodule checkouts, each at the superproject's gitlink.
set -euo pipefail
src=$1 dst=$2 rev=$3
git clone -q --no-checkout "$src" "$dst"
git -C "$dst" checkout -q --detach "$rev"
for sm in gptp-processor protocol-processor third_party/verilog-axis third_party/lwSRP third_party/tsn-c-stack; do
  pin=$(git -C "$dst" ls-tree "$rev" "$sm" | awk '{print $3}')
  git -C "$dst" config "submodule.$sm.url" "$src/$sm"
  git -C "$dst" -c protocol.file.allow=always submodule update -q --init "$sm"
  got=$(git -C "$dst/$sm" rev-parse HEAD)
  [ "$got" = "$pin" ] || { echo "PIN MISMATCH $sm $got != $pin"; exit 2; }
  echo "$sm $got"
done
git -C "$dst" rev-parse HEAD
