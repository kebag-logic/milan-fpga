#!/usr/bin/env bash
# Scratch: a clean clone of the lane at one commit, its submodules initialised from the lane's own.
# usage: clone_at.sh <new directory> <commit>
set -euo pipefail
dest=$1; commit=$2
lane=$LANES/697-consume
if [ -e "$dest" ]; then echo "exists: $dest"; exit 2; fi
git clone -q --no-hardlinks "$lane" "$dest"
cd "$dest"
git -c advice.detachedHead=false checkout -q "$commit"
for m in third_party/tsn-c-stack third_party/lwSRP protocol-processor third_party/verilog-axis gptp-processor; do
  git config "submodule.$m.url" "$lane/$m"
done
git -c protocol.file.allow=always submodule update -q --init third_party/tsn-c-stack third_party/lwSRP \
  protocol-processor third_party/verilog-axis gptp-processor
echo "$dest $(git rev-parse HEAD) dirty=$(git status --short | wc -l)"
