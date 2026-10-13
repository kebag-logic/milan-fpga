#!/usr/bin/env bash
# Scratch: a disposable clone of the lane at its HEAD with only tsn-c-stack initialised (from the lane's own
# checkout), then the lane's working files under sw/firmware/ctrl/test copied over (tracked changes and new files).
# usage: mkclone12.sh <directory>
set -euo pipefail
lane=${LANE:?LANE names the lane checkout}
dir=$(realpath -m "$1")
rm -rf "$dir"
git clone -q "$lane" "$dir"
cd "$dir"
git config submodule.third_party/tsn-c-stack.url "$lane/third_party/tsn-c-stack"
git -c protocol.file.allow=always submodule update -q --init third_party/tsn-c-stack
for f in $(git -C "$lane" status --porcelain --untracked-files=all | awk '{print $2}'); do
  cp "$lane/$f" "$dir/$f"
done
git log --oneline -1
git status --short
