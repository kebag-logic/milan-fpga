#!/usr/bin/env bash
# Extract an exact commit of the reviewed clone into a disposable tree.
# usage: extract.sh <clone> <commit> <dest>
set -euo pipefail
clone=$1; commit=$2; dest=$3
rm -rf "$dest"; mkdir -p "$dest"
git -C "$clone" archive "$commit" | tar -x -C "$dest"
echo "$commit" > "$dest/.extracted-commit"
