#!/usr/bin/env bash
# Export the exact head into a disposable tree: export_tree.sh CLONE SHA DEST
set -euo pipefail
clone=$1; sha=$2; dest=$3
rm -rf "$dest"; mkdir -p "$dest"
git -C "$clone" archive "$sha" | tar -x -C "$dest"
