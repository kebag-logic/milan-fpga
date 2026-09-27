#!/bin/bash
# Regenerate the in-tree fragments (--write-fragment) and RTL (--write-rtl) of
# every configuration in disposable base and head copies, then compare trees.
# Usage: 21_fragment_identity.sh <base-copy> <head-copy> [python]
set -u
B=${1:?base}; H=${2:?head}; PY=${3:-python3}
for T in "$B" "$H"; do
  for cfg in "$T"/configs/endstation_*.yaml; do
    n=$(basename "$cfg" .yaml)
    (cd "$T" && "$PY" sw/builder/endstation_builder.py "configs/$n.yaml" -o "$T/../frag-out-$(basename "$T")/$n" --write-fragment --write-rtl > /dev/null 2>&1); echo "$(basename "$T") $n rc=$?"
  done
done
diff -rq "$B" "$H" -x '__pycache__' | grep -v "/\.git"
echo "(expected differences: the eight files changed by the PR)"
