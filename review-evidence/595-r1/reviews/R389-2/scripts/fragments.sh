#!/usr/bin/env bash
# Hash the per-board sweep fragment written by --write-fragment after each
# tracked config, for one tree. Usage: fragments.sh <tree> <outdir>
set -euo pipefail
tree=$(cd "$1" && pwd) out=$2
for cfg in "$tree"/configs/endstation_*.yaml; do
  name=$(basename "$cfg" .yaml)
  ( cd "$tree" && python3 sw/builder/endstation_builder.py "configs/$name.yaml" --write-fragment -o "$out/$name" >/dev/null )
  frag=$(ls "$tree"/configs/generated/sweep_opts_*.sh -t | head -1)
  echo "$(sha256sum < "$frag" | cut -d' ' -f1)  $name/$(basename "$frag")"
done
