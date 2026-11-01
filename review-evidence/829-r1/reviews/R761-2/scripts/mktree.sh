#!/bin/bash
# Export one commit of the review clone plus the submodules the closed loop needs.
# usage: mktree.sh <clone> <commit> <dest>
set -eu
clone=$1; commit=$2; dest=$3
mkdir -p "$dest"
git -C "$clone" archive "$commit" | tar -x -C "$dest"
for sub in gptp-processor protocol-processor third_party/verilog-axis; do
  sha=$(git -C "$clone" rev-parse "$commit:$sub")
  mkdir -p "$dest/$sub"
  git -C "$clone/$sub" archive "$sha" | tar -x -C "$dest/$sub"
done
