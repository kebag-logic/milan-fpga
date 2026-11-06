#!/usr/bin/env bash
# collect.sh: copy the final head's runs into receipts/ with host paths scrubbed, one digest manifest per
# campaign output tree, the gate tables, and an index generated from the files present
set -u
O=$(cd "$(dirname "$0")/.." && pwd)
S=$VALIDATION_STORAGE/scratch/pp214-a736b/runs-cc92e90
R=$O/receipts
C="python3 -I $O/tools/receipt.py copy"
rm -rf "$R/proc/fast" "$R/proc/sweep" "$R/proc/area/head" "$R/campaigns" "$R/parent" "$R/parent-chain"
mkdir -p "$R/proc/area" "$R/campaigns" "$R/parent" "$R/parent-chain"
$C "$S/proc/fast" "$R/proc"
$C "$S/proc/sweep" "$R/proc"
$C "$S/proc/area/head" "$R/proc/area"
for f in "$S"/proc/area_head.*; do $C "$f" "$R/proc"; done
for f in "$S"/camps/camp-*.cmd "$S"/camps/camp-*.log "$S"/camps/camp-*.rc "$S"/camps/camp-*.start "$S"/camps/camp-*.end; do
  [ -f "$f" ] && $C "$f" "$R/campaigns"
done
for d in "$S"/camps/camp-*-out; do
  [ -d "$d" ] || continue
  (cd "$d" && find . -type f -printf '%s\t%p\n' | sort -k2 | while IFS=$'\t' read -r n p; do
     printf '%s\t%s\t%s\n' "$p" "$n" "$(sha256sum "$p" | cut -d' ' -f1)"; done) > "$R/campaigns/$(basename "$d").MANIFEST.tsv"
done
for f in "$S"/parent/rom_digests.*; do $C "$f" "$R/parent"; done
$C "$S/parent-chain/gates" "$R/parent-chain"
$C "$S/parent-chain/first-attempt-system-python" "$R/parent-chain"
cp "$O/INTERPRETER.txt" "$R/parent-chain/INTERPRETER.txt"
python3 -I "$O/tools/campdiff.py" "$R/superseded-fefb2b3/campaigns/camp-srp.log" "$R/campaigns/camp-srp.log" > "$R/campaigns/fefb2b3-vs-head.campdiff.txt"
{
  echo "# Gate table at the head"; echo
  python3 -I "$O/tools/gate_table.py" "Processor gates" "$S/proc/fast" "$S/proc/sweep" "$S/proc"
  python3 -I "$O/tools/gate_table.py" "Processor campaigns" "$S/camps"
  python3 -I "$O/tools/gate_table.py" "Scratch-parent consumer gates" "$S/parent" "$S/parent-chain/gates"
} | python3 -I -c 'import sys; sys.path.insert(0, sys.argv[1]); import receipt; sys.stdout.write(receipt.scrub(sys.stdin.read()))' "$O/tools" > "$R/GATE-TABLE.md"
# a manifest over the 200 KB limit is replaced by its own count, size and digest
for m in "$R"/campaigns/*.MANIFEST.tsv; do
  n=$(stat -c %s "$m")
  if [ "$n" -gt 204800 ]; then
    printf '%s\t%s lines\t%s bytes\tsha256 %s\tover 200 KB, not copied\n' "$(basename "$m")" "$(wc -l < "$m")" "$n" "$(sha256sum "$m" | cut -d' ' -f1)" >> "$R/campaigns/RAW-RECORDS.txt"
    rm -f "$m"
  fi
done
python3 -I "$O/tools/receipt.py" index "$O/receipts"
python3 -I "$O/tools/receipt.py" index "$O/tools"
