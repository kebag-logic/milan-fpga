#!/usr/bin/env bash
# Build the five tracked configurations from the base and head source trees at
# ONE absolute path, then hash every generated artifact.
# Usage: artifacts.sh <clone> <base-sha> <head-sha> <packet-dir>
set -euo pipefail
clone=$1 base=$2 head=$3 packet=$4
work=$packet/scratch/artifact-tree
rm -f "$packet/receipts/intree_base.sha256" "$packet/receipts/intree_head.sha256"
for rev in base head; do
  sha=$base; [ "$rev" = head ] && sha=$head
  rm -rf "$work"; mkdir -p "$work"
  git -C "$clone" archive "$sha" | tar -xf - -C "$work"
  # gitlinks are identical at both revisions; take their checked-out bytes
  for sub in protocol-processor gptp-processor third_party/verilog-axis; do
    rm -rf "${work:?}/$sub"; mkdir -p "$(dirname "$work/$sub")"
    cp -a "$clone/$sub" "$work/$sub"
  done
  for cfg in "$clone"/configs/endstation_*.yaml; do
    name=$(basename "$cfg" .yaml)
    ( cd "$work" && python3 sw/builder/endstation_builder.py "configs/$name.yaml" -o "$work/out-art" ) \
      > "$packet/receipts/build_${rev}_${name}.log" 2>&1
    # in-tree outputs (sweep fragments are per board and overwritten, so hash
    # them immediately after the config that wrote them)
    sed -n 's/^  wrote //p' "$packet/receipts/build_${rev}_${name}.log" | { grep -v '^out-art/' || true; } \
      | while read -r rel; do ( cd "$work" && sha256sum "$rel" | sed "s|^|$name |" ); done \
      >> "$packet/receipts/intree_${rev}.sha256"
  done
  ( cd "$work/out-art" && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$packet/receipts/artifacts_${rev}.sha256"
  ( cd "$work" && sha256sum configs/endstation_*.yaml ) > "$packet/receipts/configs_${rev}.sha256"
  rm -rf "$packet/scratch/out-$rev"; mv "$work/out-art" "$packet/scratch/out-$rev"
done
rm -rf "$work"
echo "artifact files base=$(wc -l < "$packet/receipts/artifacts_base.sha256") head=$(wc -l < "$packet/receipts/artifacts_head.sha256")"
if cmp -s "$packet/receipts/artifacts_base.sha256" "$packet/receipts/artifacts_head.sha256"; then echo "ARTIFACTS IDENTICAL"; else echo "ARTIFACTS DIFFER"; diff "$packet/receipts/artifacts_base.sha256" "$packet/receipts/artifacts_head.sha256" || true; fi
diff -r -q "$packet/scratch/out-base" "$packet/scratch/out-head" && echo "RAW BYTES IDENTICAL (diff -r)"
echo "in-tree files base=$(wc -l < "$packet/receipts/intree_base.sha256") head=$(wc -l < "$packet/receipts/intree_head.sha256")"
if cmp -s "$packet/receipts/intree_base.sha256" "$packet/receipts/intree_head.sha256"; then echo "IN-TREE OUTPUTS IDENTICAL"; else echo "IN-TREE OUTPUTS DIFFER"; fi
if cmp -s "$packet/receipts/configs_base.sha256" "$packet/receipts/configs_head.sha256"; then echo "CONFIGS IDENTICAL"; else echo "CONFIGS DIFFER"; fi
