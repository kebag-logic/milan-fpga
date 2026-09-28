#!/usr/bin/env bash
# Build the five tracked configurations from a base tree and a head tree,
# then hash every generated artifact. Usage: artifact_compare.sh <scratch-root>
set -u
S=${1:?scratch root holding base/ and head/ trees}
for side in base head; do
  rm -rf "$S/out-$side"; mkdir -p "$S/out-$side"
  for cfg in endstation_arty_4x4 endstation_arty_8ch endstation_arty_current \
             endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
    ( cd "$S/$side" && python3 sw/builder/endstation_builder.py \
        "configs/$cfg.yaml" -o "$S/out-$side" ) > "$S/out-$side.$cfg.log" 2>&1
    echo "$side $cfg rc=$?"
  done
  ( cd "$S/out-$side" && find . -type f | LC_ALL=C sort | xargs sha256sum ) > "$S/out-$side.sha256"
done
echo "files base=$(wc -l < "$S/out-base.sha256") head=$(wc -l < "$S/out-head.sha256")"
if diff -u "$S/out-base.sha256" "$S/out-head.sha256"; then echo "ARTIFACTS IDENTICAL"; else echo "ARTIFACTS DIFFER"; fi
diff -r -q "$S/out-base" "$S/out-head" && echo "RAW BYTES IDENTICAL (diff -r)"
