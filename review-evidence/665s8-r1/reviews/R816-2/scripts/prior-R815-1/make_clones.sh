#!/usr/bin/env bash
# Two disposable clones (base and head) of a reviewed checkout, their submodules from its local module stores.
# usage: make_clones.sh <source checkout> <dest dir> <base sha> <head sha>
set -euo pipefail
src=$1; dest=$2; base=$3; head=$4
for name in base head; do
  rev=$base; [ "$name" = head ] && rev=$head
  rm -rf "$dest/$name"
  git clone -q --no-checkout "$src" "$dest/$name"
  git -C "$dest/$name" checkout -q --detach "$rev"
  for sm in third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack; do
    git -C "$dest/$name" config "submodule.$sm.url" "$src/.git/modules/$sm"
  done
  git -C "$dest/$name" -c protocol.file.allow=always submodule update -q --init \
    third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
  echo "$name $(git -C "$dest/$name" rev-parse HEAD)"; git -C "$dest/$name" submodule status | grep -v '^-'
done
