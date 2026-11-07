#!/usr/bin/env bash
# collect.sh: copy this head's runs into receipts/ with host paths scrubbed, one digest manifest for the campaign's
# output tree, the gate tables, the per-arm failing rows, and an index generated from the files present
set -u
O=$(cd "$(dirname "$0")/.." && pwd)
S=$VALIDATION_STORAGE/scratch/pp214-a736d/runs
R=$O/receipts
C="python3 -I $O/tools/receipt.py copy"
rm -rf "$R/proc" "$R/campaigns" "$R/parent" "$R/parent-chain" "$R/arms"
mkdir -p "$R/campaigns" "$R/parent" "$R/parent-chain" "$R/arms"
$C "$S/proc" "$R"
for f in "$S"/camp/camp-srp.cmd "$S"/camp/camp-srp.log "$S"/camp/camp-srp.rc "$S"/camp/camp-srp.start "$S"/camp/camp-srp.end "$S"/camp/camp-srp.python; do $C "$f" "$R/campaigns"; done
(cd "$S/camp/camp-srp-out" && find . -type f -printf '%s\t%p\n' | sort -k2 | while IFS=$'\t' read -r n p; do
   printf '%s\t%s\t%s\n' "$p" "$n" "$(sha256sum "$p" | cut -d' ' -f1)"; done) > "$R/campaigns/camp-srp-out.MANIFEST.tsv"
for f in "$S"/parent/rom_digests.* "$S"/parent/head.txt; do $C "$f" "$R/parent"; done
$C "$S/parent/gates" "$R/parent-chain"
$C "$S/head-arms/reviewer-arms.tsv" "$R/arms"
$C "$S/head-arms/encoder-arm-counts.tsv" "$R/arms"
for arm in msrp-read-taken-by-any-search mvrp-read-taken-by-any-search search-survives-accept identity-drops-top-octet \
    identity-vid-low-octet-only merge-keeps-older-value mvrp-merge-never-written mvrp-lv-keeps-joinin mvrp-lv-keeps-new \
    mvrp-new-keeps-lv listener-type-s-over-s-kept unknown-type-held-while-pending push-on-drain-start second-queueing; do
  { echo "== $arm"; grep -E '^[0-9]+ checks:' "$S/head-arms/enc/$arm.log"; grep '^FAIL' "$S/head-arms/enc/$arm.log" | cut -c1-150; echo; }
done > "$R/arms/new-arm-failing-words.txt"
{ echo "tb/srp_encoder at the head with main 92100657's encoder"; grep -E '^[0-9]+ checks:' "$S/head-arms/enc/BASE.log"; grep '^FAIL' "$S/head-arms/enc/BASE.log" | cut -c1-150; } > "$R/arms/base-encoder.txt"
{
  echo "# Gate table at the head"; echo
  python3 -I "$O/tools/gate_table.py" "Processor gates" "$S/proc"
  python3 -I "$O/tools/gate_table.py" "SRP mutant campaign" "$S/camp"
  python3 -I "$O/tools/gate_table.py" "Scratch-parent consumer gates" "$S/parent" "$S/parent/gates"
} | python3 -I -c 'import sys; sys.path.insert(0, sys.argv[1]); import receipt; sys.stdout.write(receipt.scrub(sys.stdin.read()))' "$O/tools" > "$R/GATE-TABLE.md"
m=$R/campaigns/camp-srp-out.MANIFEST.tsv; n=$(stat -c %s "$m")
if [ "$n" -gt 204800 ]; then
  printf '%s\t%s lines\t%s bytes\tsha256 %s\tover 200 KB, not copied\n' "$(basename "$m")" "$(wc -l < "$m")" "$n" "$(sha256sum "$m" | cut -d' ' -f1)" >> "$R/campaigns/RAW-RECORDS.txt"
  rm -f "$m"
fi
python3 -I "$O/tools/receipt.py" index "$O/receipts"
python3 -I "$O/tools/receipt.py" index "$O/tools"
