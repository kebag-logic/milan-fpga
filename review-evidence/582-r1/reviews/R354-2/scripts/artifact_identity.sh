#!/bin/bash
# R354-1: build the five tracked configurations with each tree's own builder
# (source base and exact head, both extracted by `git archive` with identical
# submodule contents), then compare every generated file byte for byte.
# Usage: artifact_identity.sh <base-tree> <head-tree> <python>
set -euo pipefail
BASE=$1; HEAD=$2; PY=$3
for tree in "$BASE" "$HEAD"; do
  (
    cd "$tree"
    for cfg in configs/endstation_*.yaml; do
      name=$(basename "$cfg" .yaml)
      "$PY" sw/builder/endstation_builder.py "$cfg" -o "ART/$name" --write-fragment > "ART.$name.log" 2>&1
    done
    find ART configs/generated -type f -print0 | sort -z | xargs -0 sha256sum > ART.sha256
  )
done
echo "base files: $(wc -l < "$BASE/ART.sha256")  head files: $(wc -l < "$HEAD/ART.sha256")"
if cmp -s "$BASE/ART.sha256" "$HEAD/ART.sha256"; then
  echo "IDENTICAL: every generated file of the five configurations matches"
else
  diff "$BASE/ART.sha256" "$HEAD/ART.sha256" || true
  echo "DIFFERENT"
  exit 1
fi
