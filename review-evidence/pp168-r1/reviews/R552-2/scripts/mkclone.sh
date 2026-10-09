#!/usr/bin/env bash
# Make a disposable, detached clone of the reviewed head (or another rev).
# usage: mkclone.sh SOURCE_REPO DEST_DIR REV
set -euo pipefail
src=$1; dest=$2; rev=$3
rm -rf "$dest"
git clone -q --no-hardlinks --no-checkout "$src" "$dest"
git -C "$dest" checkout -q --detach "$rev"
test "$(git -C "$dest" rev-parse HEAD)" = "$(git -C "$src" rev-parse "$rev")"
echo "clone $dest at $(git -C "$dest" rev-parse HEAD) tree $(git -C "$dest" rev-parse 'HEAD^{tree}')"
