#!/bin/sh
# Build the five tracked configurations with the base and the head builder,
# each from its own exported tree, into separate output roots, then compare
# every artifact and the tree's tracked files after the build.
# Usage: byte_identity.sh <scratch dir holding base/ and head/>
S=$1
for t in base head; do
  rm -rf "$S/bi-$t"; mkdir -p "$S/bi-$t"
  for c in "$S/$t"/configs/endstation_*.yaml; do
    n=$(basename "$c" .yaml)
    (cd "$S/$t" && python3 sw/builder/endstation_builder.py -o "$S/bi-$t" "configs/$n.yaml") \
      > "$S/bi-$t.$n.log" 2>&1; echo "$t $n builder rc=$?"
  done
done
echo "files base=$(find "$S/bi-base" -type f | wc -l) head=$(find "$S/bi-head" -type f | wc -l)"
diff -r "$S/bi-base" "$S/bi-head" && echo "diff -r artifacts rc=0"
(cd "$S/bi-base" && find . -type f | sort | xargs sha256sum) > "$S/bi-base.sha256"
(cd "$S/bi-head" && find . -type f | sort | xargs sha256sum) > "$S/bi-head.sha256"
cmp "$S/bi-base.sha256" "$S/bi-head.sha256" && echo "sha256 lists identical"
