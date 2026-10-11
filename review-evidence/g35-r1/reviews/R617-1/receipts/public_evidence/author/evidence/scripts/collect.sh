#!/usr/bin/env bash
# Copy small evidence files into the output directory (each well under
# 200 KB); large logs are recorded by sha256 and size instead.
set -u
S=$VALIDATION_STORAGE/g35-a599
O=$MANAGEMENT/2026-09-23/g35-a599/evidence
mkdir -p "$O/gates-base" "$O/gates-head" "$O/parent/base" "$O/parent/head" \
         "$O/equiv" "$O/mutation" "$O/scripts"
for side in base head; do
  for f in identity.txt contract.log lint.log docs.log tb.log; do
    [ -f "$S/gates-$side/$f" ] && cp "$S/gates-$side/$f" "$O/gates-$side/"
  done
  for g in contract lint docs tb; do
    [ -f "$S/gates-$side/$g.rc" ] && echo "$g rc=$(cat "$S/gates-$side/$g.rc")"
  done > "$O/gates-$side/rc.txt"
  P=$O/parent/$side
  sed "s|$S/parent|<scratch-parent>|g" "$S/parent-$side/identity.txt" > "$P/identity.txt"
  cp "$S/parent-$side/gate.log" "$S/parent-$side/rom_sha256.txt" \
     "$S/parent-$side/rom_bundle_digest.txt" "$S/parent-$side/netlist_sha256.txt" "$P/"
  cp "$S/parent-$side/results/top-KL_gptp_shadow.result" "$P/"
  cp "$S/parent-$side/work/hier.stat.txt" "$S/parent-$side/work/flat.stat.txt" "$P/"
  for g in gate sv2v enforce rom_bundle hier flat; do
    echo "$g rc=$(cat "$S/parent-$side/$g.rc")"
  done > "$P/rc.txt"
done
cp "$S/module-compare.txt" "$O/parent/"
cp "$S/equiv/equiv_tied.ys" "$S/equiv/equiv_free.ys" "$S/equiv/shadow_equiv_tied.ys" \
   "$S/equiv/shadow_equiv_free.ys" "$S/equiv/wrap_base_tied.v" "$S/equiv/wrap_head_tied.v" \
   "$S/equiv/wrap_base_free.v" "$S/equiv/wrap_head_free.v" "$O/equiv/"
{
  for l in equiv_tied equiv_free shadow_equiv_tied shadow_equiv_free; do
    echo "== $l.log ($(stat -c %s "$S/equiv/$l.log") bytes, sha256 $(sha256sum < "$S/equiv/$l.log" | cut -c1-64))"
    grep -E "Of those cells|Unproven \\\$equiv|ERROR" "$S/equiv/$l.log"
  done
} > "$O/equiv/summary.txt"
cp "$S/per-position.tsv" "$S/planted-control.log" "$O/mutation/" 2>/dev/null
cp "$S/meta2/reverted.log" "$O/mutation/arm-with-repair-reverted.log"
cp "$S/meta2/renamed.log" "$O/mutation/arm-with-a-named-check-renamed.log"
cp "$S/bin/gates.sh" "$S/bin/parent_evidence.sh" "$S/bin/planted_control.sh" \
   "$S/bin/collect.sh" "$O/scripts/"
find "$O" -type f -size +200k -print
du -sh "$O"
# the parent's own ROM-digest check (ooc.sh, ledger keyed by the pin)
mkdir -p "$O/parent/romcheck"
for f in head-check-unrecorded head-record head-check-recorded base-check; do
  sed "s|$S/parent|<scratch-parent>|g; s|$S/tmp|<scratch-tmp>|g" "$S/romcheck/$f.log" > "$O/parent/romcheck/$f.log"
  cp "$S/romcheck/$f.rc" "$O/parent/romcheck/$f.rc"
done
cp "$S/romcheck/head-record.diff" "$O/parent/romcheck/"
find "$O" -type f -size +200k -print
