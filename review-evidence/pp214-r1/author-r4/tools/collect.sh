#!/usr/bin/env bash
# collect.sh: copy this head's runs into receipts/ with host paths scrubbed, one digest manifest for the campaign's
# output tree, the gate tables, the per-arm failing rows, and an index generated from the files present
set -u
O=$(cd "$(dirname "$0")/.." && pwd)
S=$VALIDATION_STORAGE/scratch/pp214-a736e/runs
R=$O/receipts
P3=$O/../pp214-a736d/receipts
C="python3 -I -B $O/tools/receipt.py copy"
rm -rf "$R/proc" "$R/campaigns" "$R/parent" "$R/parent-chain" "$R/arms"
mkdir -p "$R/campaigns" "$R/parent" "$R/parent-chain" "$R/arms"
$C "$S/proc" "$R"
for f in "$S"/camp/camp-srp.cmd "$S"/camp/camp-srp.log "$S"/camp/camp-srp.rc "$S"/camp/camp-srp.start "$S"/camp/camp-srp.end "$S"/camp/camp-srp.python; do $C "$f" "$R/campaigns"; done
(cd "$S/camp/camp-srp-out" && find . -type f -printf '%s\t%p\n' | sort -k2 | while IFS=$'\t' read -r n p; do
   printf '%s\t%s\t%s\n' "$p" "$n" "$(sha256sum "$p" | cut -d' ' -f1)"; done) > "$R/campaigns/camp-srp-out.MANIFEST.tsv"
python3 -I -B "$O/tools/campdiff.py" "$P3/campaigns/camp-srp.log" "$S/camp/camp-srp.log" > "$R/campaigns/1c8b485-vs-head.campdiff.txt"
for f in "$S"/parent/rom_digests.* "$S"/parent/head.txt; do $C "$f" "$R/parent"; done
$C "$S/parent/gates" "$R/parent-chain"
$C "$S/rv-r1.tsv" "$R/arms"
mv "$R/arms/rv-r1.tsv" "$R/arms/first-reviews-52-arms.tsv"
$C "$S/rv2/SUMMARY.tsv" "$R/arms"; mv "$R/arms/SUMMARY.tsv" "$R/arms/second-reviews-arms-and-bit-walk.tsv"
$C "$S/enc3.tsv" "$R/arms"; mv "$R/arms/enc3.tsv" "$R/arms/encoder-arm-counts.tsv"
for arm in push-on-prepared-start push-taken-in-alloc push-on-drain-start second-queueing identity-drops-top-octet identity-vid-low-octet-only; do
  { echo "== $arm"; grep -E '^[0-9]+ checks:' "$S/enc3/$arm.log"; grep '^FAIL' "$S/enc3/$arm.log" | cut -c1-150; echo; }
done > "$R/arms/new-arm-failing-words.txt"
{ echo "tb/srp_encoder at the head with main 92100657's encoder (identical to a9e84b66's)"; grep -E '^[0-9]+ checks:' "$S/enc3/BASE.log"; grep '^FAIL' "$S/enc3/BASE.log" | cut -c1-150; } > "$R/arms/base-encoder.txt"
{ echo "The two new arms against the suite of 1c8b485 (this round's rows absent): each survives"
  for arm in push-on-prepared-start push-taken-in-alloc; do printf '%s\t%s\n' "$arm" "$(grep -E '^[0-9]+ checks:' "$S/before/$arm.at-1c8b485-suite.log")"; done; } > "$R/arms/new-arms-against-the-1c8b485-suite.txt"
{ echo "rv-empty-table-searches at the head: the first named failures and the tally"; grep '^FAIL' "$S/rv2/rv-empty-table-searches.log" | head -8 | cut -c1-120; grep -E '^[0-9]+ checks:' "$S/rv2/rv-empty-table-searches.log"; } > "$R/arms/rv-empty-table-searches.txt"
{
  echo "# Gate table at the head"; echo
  python3 -I -B "$O/tools/gate_table.py" "Processor gates" "$S/proc"
  python3 -I -B "$O/tools/gate_table.py" "SRP mutant campaign" "$S/camp"
  python3 -I -B "$O/tools/gate_table.py" "Scratch-parent consumer gates" "$S/parent" "$S/parent/gates"
} | python3 -I -B -c 'import sys; sys.path.insert(0, sys.argv[1]); import receipt; sys.stdout.write(receipt.scrub(sys.stdin.read()))' "$O/tools" > "$R/GATE-TABLE.md"
m=$R/campaigns/camp-srp-out.MANIFEST.tsv; n=$(stat -c %s "$m")
if [ "$n" -gt 204800 ]; then
  printf '%s\t%s lines\t%s bytes\tsha256 %s\tover 200 KB, not copied\n' "$(basename "$m")" "$(wc -l < "$m")" "$n" "$(sha256sum "$m" | cut -d' ' -f1)" >> "$R/campaigns/RAW-RECORDS.txt"
  rm -f "$m"
fi
rm -rf "$O/tools/__pycache__"
python3 -I -B "$O/tools/receipt.py" index "$O/receipts"
python3 -I -B "$O/tools/receipt.py" index "$O/tools"
