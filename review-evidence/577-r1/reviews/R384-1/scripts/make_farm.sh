#!/bin/sh
# Build a symlink-farm probe root from a checkout, with sw/builder as real copies
# so a mutated file is the one imported. Usage: make_farm.sh <checkout> <dest>
set -eu
src=$(cd "$1" && pwd); dest=$2
rm -rf "$dest"; mkdir -p "$dest"
for e in "$src"/* "$src"/.[!.]*; do
  n=$(basename "$e"); [ "$n" = .git ] && continue; [ -e "$e" ] || continue
  if [ -d "$e" ]; then cp -as "$e" "$dest/$n"; else ln -s "$e" "$dest/$n"; fi
done
rm -rf "$dest/sw/builder"; mkdir -p "$dest/sw/builder"
for f in "$src"/sw/builder/*.py; do cp "$f" "$dest/sw/builder/"; done
# gen_ucode.py as a real copy so consumer-derivation probes can edit it
g=protocol-processor/hdl/aecp/ucode/gen_ucode.py
rm -f "$dest/$g"; cp "$src/$g" "$dest/$g"
