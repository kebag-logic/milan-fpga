#!/usr/bin/env bash
# Build all five shipping configurations' builder outputs and AEM images from
# two exported trees and compare every file's bytes.
#   old: parent 682ecf0c + protocol-processor 870ff88a
#   new: parent 499b15f9 + protocol-processor 16be6768
# gptp-processor and verilog-axis at their (unchanged) gitlinks in both trees.
# Usage: pin_equality.sh <parent clone> <work dir> <receipt dir>
set -u
CLONE=$1; WORK=$2; OUT=$3
BASE=682ecf0cb995473b72d5b4921088053ba753fc93
HEAD=499b15f97eb0a469b7cd1308fbba7af3c64d1851
rm -rf "$WORK"; mkdir -p "$WORK"
export PYTHONDONTWRITEBYTECODE=1
for side in old new; do
  if [ $side = old ]; then P=$BASE; else P=$HEAD; fi
  T="$WORK/$side/tree"; mkdir -p "$T"
  git -C "$CLONE" archive "$P" | tar -x -C "$T" || exit 2
  for sub in protocol-processor gptp-processor third_party/verilog-axis; do
    pin=$(git -C "$CLONE" rev-parse "$P:$sub") || exit 2
    echo "$side $sub $pin" >> "$OUT/pin-equality-inputs.txt"
    mkdir -p "$T/$sub"
    git -C "$CLONE/$sub" archive "$pin" | tar -x -C "$T/$sub" || exit 2
  done
  echo "$side parent $P" >> "$OUT/pin-equality-inputs.txt"
  for cfg in "$T"/configs/endstation_*.yaml; do
    name=$(basename "$cfg" .yaml)
    R="$WORK/$side/run/$name"; mkdir -p "$R"
    (cd "$T" && python3 sw/builder/endstation_builder.py "configs/$name.yaml" -o "$R/builder") \
      > "$R/builder.log" 2>&1; rc1=$?
    (cd "$T" && python3 avdecc/gen_aemi_image.py --overlay "$R/builder/$name/aem_overlay.json" \
      --line-bytes 576 -o "$R/aem.bin" -m "$R/aem.map" --json "$R/aem.json") \
      > "$R/aem.log" 2>&1; rc2=$?
    echo "$side $name builder_rc=$rc1 aem_rc=$rc2" >> "$OUT/pin-equality-rcs.txt"
  done
  (cd "$WORK/$side/run" && find . -type f ! -name '*.log' | LC_ALL=C sort | \
     xargs sha256sum) > "$OUT/pin-equality-$side.sha256"
done
if diff -u "$OUT/pin-equality-old.sha256" "$OUT/pin-equality-new.sha256" > "$OUT/pin-equality.diff"; then
  n=$(wc -l < "$OUT/pin-equality-new.sha256")
  # Hash equality is re-confirmed on bytes.
  bad=0
  while read -r _ f; do cmp -s "$WORK/old/run/$f" "$WORK/new/run/$f" || { echo "BYTES DIFFER $f"; bad=1; }; done \
    < "$OUT/pin-equality-new.sha256"
  [ $bad -eq 0 ] && echo "IDENTICAL: $n files byte-equal between old and new pins"
else
  echo "DIFFERENT: see pin-equality.diff"; exit 1
fi
