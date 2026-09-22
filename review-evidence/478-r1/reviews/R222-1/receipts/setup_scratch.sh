#!/usr/bin/env bash
# [R222] isolated scratch clones for focused probes. Reads the review clone's
# object stores only; never writes to it. Usage: setup_scratch.sh <commit> <dir>
# The three required submodules are registered and checked out at the
# superproject's gitlinks (git submodule status prints no '-'/'+'/'U' prefix),
# cloned from the review clone's own module stores, never from the network.
set -euo pipefail
src=$VALIDATION_STORAGE/reviews/r222-478-r1
commit=$1
dir=$2
rm -rf "$dir"
git clone --quiet --no-hardlinks --no-checkout "$src" "$dir"
git -C "$dir" checkout --quiet --detach "$commit"
for sub in protocol-processor gptp-processor third_party/verilog-axis; do
    git -C "$dir" config "submodule.$sub.url" "$src/.git/modules/$sub"
done
git -C "$dir" -c protocol.file.allow=always submodule --quiet update --init \
    protocol-processor gptp-processor third_party/verilog-axis
git -C "$dir" submodule status
echo "superproject $(git -C "$dir" rev-parse HEAD) tree $(git -C "$dir" rev-parse 'HEAD^{tree}')"
