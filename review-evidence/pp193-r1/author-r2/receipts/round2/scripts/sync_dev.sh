#!/usr/bin/env bash
# copy the lane's working tree (tracked files, as edited) into a scratch tree
# usage: sync_dev.sh <dest>
set -eu
dest=$1
lane=<lane>
mkdir -p "$dest"
cd "$lane"
git ls-files -z | rsync -a --from0 --files-from=- ./ "$dest/"
