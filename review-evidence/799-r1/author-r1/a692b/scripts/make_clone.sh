#!/usr/bin/env bash
# A clean clone of the #799 lane at one revision, its initialised submodules
# taken from the lane's own checkouts (no network).
# usage: make_clone.sh <dest> <rev>
set -euo pipefail
lane=$LANES/799-adopt6
dest=$1; rev=$2
test ! -e "$dest"
git clone -q --no-checkout "$lane" "$dest"
git -C "$dest" checkout -q --detach "$rev"
# the validation base: the lane's origin/dev, the live remote dev tip, as origin/dev and dev here
git -C "$dest" fetch -q "$lane" refs/remotes/origin/dev:refs/remotes/origin/dev
git -C "$dest" branch -q -f dev refs/remotes/origin/dev
for sm in third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack; do
  git -C "$dest" config "submodule.$sm.url" "$lane/$sm"
  git -C "$dest" -c protocol.file.allow=always submodule update -q --init "$sm"
done
git -C "$dest" rev-parse HEAD
git -C "$dest" submodule status
git -C "$dest" status --short | head
