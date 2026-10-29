#!/bin/bash
# sync.sh <dest>: a fresh clone of the lane at HEAD plus its working-tree changes
set -euo pipefail
lane=<lane>
dest=$1
rm -rf "$dest"
git clone -q "$lane" "$dest"
git -C "$lane" diff HEAD --binary > "$dest.diff"
if [ -s "$dest.diff" ]; then git -C "$dest" apply --whitespace=nowarn "$dest.diff"; fi
git -C "$lane" ls-files --others --exclude-standard -z | (cd "$lane" && xargs -0 -r cp --parents -t "$dest")
rm -f "$dest.diff"
git -C "$dest" status --short | head -20
