#!/bin/sh
# Build both shipped configs' default artifacts from two trees with one fixed config path each, then compare hashes.
# usage: builder_identity.sh <treeA> <treeB> <workdir>
set -eu
A=$1; B=$2; W=$3
for t in A B; do
  eval tree=\$$t
  for c in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
    mkdir -p "$W/cfg/$c" "$W/out-$t/$c"
    cp "$tree/configs/$c.yaml" "$W/cfg/$c/$c.yaml"
    (cd "$tree" && python3 sw/builder/endstation_builder.py -o "$W/out-$t/$c" "$W/cfg/$c/$c.yaml" > "$W/build-$t-$c.log" 2>&1)
  done
done
for c in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
  (cd "$W/out-A/$c" && find . -type f | sort | xargs sha256sum) > "$W/hash-A-$c.txt"
  (cd "$W/out-B/$c" && find . -type f | sort | xargs sha256sum) > "$W/hash-B-$c.txt"
  n=$(wc -l < "$W/hash-A-$c.txt")
  if cmp -s "$W/hash-A-$c.txt" "$W/hash-B-$c.txt"; then echo "$c: $n files IDENTICAL"; else echo "$c: DIFFER"; diff "$W/hash-A-$c.txt" "$W/hash-B-$c.txt" || true; fi
done
