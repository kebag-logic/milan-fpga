#!/bin/bash
# usage: mkclone.sh <dest>  -- clone the scratch parent snapshot with its submodules from parent-work
set -euo pipefail
S=<scratch>; SRC=$S/parent-work; D=$1
git clone -q "$SRC" "$D"
cd "$D"
git checkout -q "$(git -C "$SRC" rev-parse HEAD)"
for m in third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack; do
  git config "submodule.$m.url" "$SRC/$m"
  git -c protocol.file.allow=always submodule update -q --init "$m"
done
git submodule status
git status --short | wc -l
