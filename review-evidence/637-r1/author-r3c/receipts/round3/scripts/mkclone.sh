#!/usr/bin/env bash
# a clean clone of the lane at <rev>, its populated submodules taken from the lane's own checkouts
# usage: mkclone.sh <dest> <rev>
set -eu
L=<lane>
dest=$1; rev=$2
rm -rf "$dest"
git clone -q --no-checkout "$L" "$dest"
cd "$dest"
git checkout -q --detach "$rev"
for s in gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis; do
  git config "submodule.$s.url" "$L/$s"
done
git -c protocol.file.allow=always submodule update -q --init gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
# then each origin back to the .gitmodules URL, as a clone of the canonical repository has it
git submodule sync -q
git rev-parse HEAD; git status --short; git submodule status
