#!/bin/bash
# Build every tracked configuration with the base and the head builder CLI and
# compare the complete output trees byte-for-byte (every file, recursively).
# Usage: 20_artifact_identity.sh <base-tree> <head-tree> <out-dir> [python]
set -u
B=${1:?base}; H=${2:?head}; O=${3:?out}; PY=${4:-python3}
rm -rf "$O"; mkdir -p "$O"
rc=0
for cfg in "$H"/configs/endstation_*.yaml; do
  n=$(basename "$cfg" .yaml)
  cmp -s "$cfg" "$B/configs/$n.yaml" || { echo "CONFIG DIFFERS $n"; rc=1; }
  for side in base head; do
    T=$B; [ $side = head ] && T=$H
    (cd "$T" && "$PY" sw/builder/endstation_builder.py "configs/$n.yaml" -o "$O/$side/$n" > "$O/$side-$n.log" 2>&1); echo "build $side $n rc=$?"
  done
  (cd "$O/base/$n" && find . -type f | LC_ALL=C sort | xargs sha256sum) > "$O/$n.base.sha256"
  (cd "$O/head/$n" && find . -type f | LC_ALL=C sort | xargs sha256sum) > "$O/$n.head.sha256"
  if cmp -s "$O/$n.base.sha256" "$O/$n.head.sha256" && diff -r "$O/base/$n" "$O/head/$n" > /dev/null; then
    echo "IDENTICAL $n files=$(wc -l < "$O/$n.head.sha256") tree-sha256=$(sha256sum < "$O/$n.head.sha256" | cut -d' ' -f1)"
  else echo "DIFFERS $n"; diff "$O/$n.base.sha256" "$O/$n.head.sha256"; rc=1; fi
done
echo "identity rc=$rc"; exit $rc
