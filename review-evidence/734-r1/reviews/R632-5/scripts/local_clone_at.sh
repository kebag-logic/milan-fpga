#!/usr/bin/env bash
# Make a disposable clone of <repo> at <commit> with its public submodules materialized
# from <repo>'s own module stores (no network). Usage: local_clone_at.sh <repo> <commit> <dest>
set -euo pipefail
repo=$1 commit=$2 dest=$3
rm -rf "$dest"
git clone --quiet --no-checkout "$repo" "$dest"
git -C "$dest" -c advice.detachedHead=false checkout --quiet "$commit"
git -C "$dest" submodule init >/dev/null
for name in third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack; do
  # Only submodules the source checkout has materialized have a module store to copy from.
  if [ -e "$repo/$name/.git" ] && git -C "$dest" ls-tree "$commit" "$name" | grep -q '^160000'; then
    git -C "$dest" config "submodule.$name.url" "$(git -C "$repo/$name" rev-parse --absolute-git-dir)"
    git -C "$dest" -c protocol.file.allow=always submodule update --quiet "$name"
  fi
done
git -C "$dest" submodule status
