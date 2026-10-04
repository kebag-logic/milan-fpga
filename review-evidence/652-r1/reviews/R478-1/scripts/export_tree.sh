#!/bin/sh
# Export one commit of the review clone, with its pinned submodules, into a
# disposable directory. Usage: export_tree.sh <clone> <commit> <dest>
set -eu
clone=$1; rev=$2; dest=$3
rm -rf "$dest"; mkdir -p "$dest"
git -C "$clone" archive "$rev" | tar -x -C "$dest"
for sm in third_party/verilog-axis protocol-processor gptp-processor; do
  sha=$(git -C "$clone" rev-parse "$rev:$sm")
  mkdir -p "$dest/$sm"
  git -C "$clone/$sm" archive "$sha" | tar -x -C "$dest/$sm"
  echo "$sm $sha"
done
