#!/usr/bin/env bash
# Scratch: a clean clone of the lane at one commit with only the submodules the hosted docs job fetches.
# usage: clone_docs_at.sh <new directory> <commit>
set -euo pipefail
dest=$1; commit=$2
lane=$LANES/697-consume
if [ -e "$dest" ]; then echo "exists: $dest"; exit 2; fi
git clone -q --no-hardlinks "$lane" "$dest"
cd "$dest"
git -c advice.detachedHead=false checkout -q "$commit"
for m in protocol-processor third_party/verilog-axis gptp-processor; do
  git config "submodule.$m.url" "$lane/$m"
done
git -c protocol.file.allow=always submodule update -q --init protocol-processor third_party/verilog-axis gptp-processor
echo "$dest $(git rev-parse HEAD) dirty=$(git status --short | wc -l)"
