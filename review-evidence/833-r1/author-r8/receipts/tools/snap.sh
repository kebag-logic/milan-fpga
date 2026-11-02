#!/usr/bin/env bash
# Snapshot the lane's HEAD plus its uncommitted diff into a fresh scratch clone.
# usage: snap.sh <name>   -> $VALIDATION_STORAGE/833-a726h/wt-<name>
set -eu
lane=$LANES/833-owned-process
dest=$VALIDATION_STORAGE/833-a726h/wt-$1
rm -rf "$dest"
git clone -q --no-hardlinks "$lane" "$dest"
git -C "$dest" checkout -q "$(git -C "$lane" rev-parse HEAD)"
git -C "$lane" diff HEAD > "$dest.patch"
[ -s "$dest.patch" ] && git -C "$dest" apply "$dest.patch"
git -C "$dest" status --short
echo "$dest at $(git -C "$dest" rev-parse HEAD)"
