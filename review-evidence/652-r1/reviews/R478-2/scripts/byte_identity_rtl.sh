#!/bin/sh
# For each tracked configuration, run the base and the head builder with
# --write-rtl --write-fragment, each in its own fresh copy of its exported
# tree, into its own output root. Compare, base against head: every output
# artifact, and every tracked-tree file the run rewrote (found by diff -rq
# against the pristine export). Usage: byte_identity_rtl.sh <scratch dir>
S=$1; rc=0
for c in "$S"/head/configs/endstation_*.yaml; do
  n=$(basename "$c" .yaml)
  for t in base head; do
    W=$S/bir-$t-$n; rm -rf "$W"; cp -a "$S/$t" "$W/"
    (cd "$W" && python3 sw/builder/endstation_builder.py -o "$S/bir-out-$t-$n" --write-rtl --write-fragment \
      "configs/$n.yaml") > "$S/bir-$t-$n.log" 2>&1; echo "$t $n builder rc=$?"
    diff -rq "$S/$t" "$W" > "$S/bir-$t-$n.touched"; sed "s|$S/||g" "$S/bir-$t-$n.touched" > "$S/bir-$t-$n.touched.rel"
  done
  echo "$n tracked files rewritten differently from the export: base=$(wc -l < "$S/bir-base-$n.touched") head=$(wc -l < "$S/bir-head-$n.touched")"
  for f in $(awk '/^Files/{print $2}' "$S/bir-head-$n.touched" | sed "s|$S/head/||"); do
    cmp "$S/bir-base-$n/$f" "$S/bir-head-$n/$f" || rc=1; echo "  $f: base and head regenerate identical bytes (cmp rc=$?)"
  done
  sed "s|bir-base-$n|X|;s|base/|T/|" "$S/bir-base-$n.touched.rel" > "$S/a.t"; sed "s|bir-head-$n|X|;s|head/|T/|" "$S/bir-head-$n.touched.rel" > "$S/b.t"
  cmp -s "$S/a.t" "$S/b.t" && echo "  touched-file sets equal" || { echo "  touched-file sets DIFFER"; rc=1; }
  diff -r "$S/bir-out-base-$n" "$S/bir-out-head-$n" > /dev/null && echo "  outputs identical ($(find "$S/bir-out-head-$n" -type f | wc -l) files)" || { echo "  outputs DIFFER"; rc=1; }
done
echo "byte_identity_rtl overall rc=$rc"; exit $rc
