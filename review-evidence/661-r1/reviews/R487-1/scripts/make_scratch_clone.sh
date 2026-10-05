#!/usr/bin/env bash
# Disposable shared clone of the review checkout with its three submodules at the recorded gitlinks.
# Usage: make_scratch_clone.sh <review-clone> <dest> <rev> [<merge-rev>]
# With <merge-rev>, the clone stages `git merge --no-commit <merge-rev>` on top of <rev>: a merge
# candidate in the index and work tree, never committed.
set -eu
src=$1; dst=$2; rev=$3; mrg=${4:-}
rm -rf "$dst"; git clone -q --shared --no-checkout "$src" "$dst"
git -C "$dst" checkout -q --detach "$rev"
if [ -n "$mrg" ]; then
  git -C "$dst" fetch -q "$src" "$mrg"
  git -C "$dst" -c user.name=probe -c user.email=probe@invalid merge -q --no-commit --no-ff "$mrg"
fi
for sm in protocol-processor gptp-processor third_party/verilog-axis; do
  git -C "$dst" config "submodule.$sm.url" "$src/$sm"
done
git -C "$dst" -c protocol.file.allow=always submodule -q update --init protocol-processor gptp-processor third_party/verilog-axis
git -C "$dst" submodule status
git -C "$dst" status --short | head -5
