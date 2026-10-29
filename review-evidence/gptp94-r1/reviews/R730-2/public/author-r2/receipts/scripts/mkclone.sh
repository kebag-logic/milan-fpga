#!/bin/bash
# usage: mkclone.sh <src parent> <dest> <rev>: clone the scratch parent at
# <rev> with its public submodules taken from the source's own checkouts
set -euo pipefail
SRC=$1; D=$2; REV=$3
git clone -q "$SRC" "$D"
cd "$D"
git -c advice.detachedHead=false checkout -q "$REV"
for m in third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack; do
  git config "submodule.$m.url" "$SRC/$m"
  git -c protocol.file.allow=always submodule update -q --init "$m"
done
git rev-parse HEAD
git submodule status
