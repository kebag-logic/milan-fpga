#!/usr/bin/env bash
# Scratch: a clean clone of the lane at a given revision, with the given submodules (default: tsn-c-stack only),
# each from the lane's own checkout.
# usage: mkclone14.sh <directory> <revision> [submodule...]
set -euo pipefail
lane=$LANES/697-consume
dir=$1; rev=$2; shift 2
subs=("${@:-third_party/tsn-c-stack}")
rm -rf "$dir"
git clone -q "$lane" "$dir"
cd "$dir"
git checkout -q --detach "$(git -C "$lane" rev-parse "$rev^{commit}")"
for sub in "${subs[@]}"; do git config "submodule.$sub.url" "$lane/$sub"; done
git -c protocol.file.allow=always submodule update -q --init "${subs[@]}"
git log --oneline -1 | cut -c1-60
git submodule status -- "${subs[@]}"
