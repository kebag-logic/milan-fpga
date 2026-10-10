#!/bin/sh
# Re-run every round 2 recompute and compare with outputs/ byte for byte.
# usage: run_all.sh <packet-author-dir> <out-dir> [<raw-root>]
# <packet-author-dir> is review-evidence/608-b14-r1/author/ extracted from the archive.
# <raw-root> (optional) holds item3/cycle-NNN/tap.pcap; those captures are not public.
set -eu
H=$(cd "$(dirname "$0")/.." && pwd)
A=$1
O=$2
RAW=${3:-}
mkdir -p "$O"
python3 -I "$H/scripts/inputs_vs_index.py" check "$H/inputs/raw-inputs.tsv" "$A/raw-index" "$H/inputs" > "$O/inputs_check.txt"
python3 -I "$H/scripts/final_vs_asfound.py" "$A" "$H/inputs/snapshot-final.jsonl" > "$O/final_vs_asfound.txt"
python3 -I "$H/scripts/inventory_rows.py" "$H/inputs/snapshot-prebind.jsonl" "$H/inputs/snapshot-final.jsonl" > "$O/inventory_rows.txt"
python3 -I "$H/scripts/slip_ledger.py" "$A" > "$O/slip_ledger.txt"
python3 -I "$H/scripts/ta_lv_vs_cycles.py" "$H/outputs/ta_lv_all.txt" "$A" > "$O/ta_lv_vs_cycles.txt"
for f in inputs_check.txt final_vs_asfound.txt inventory_rows.txt slip_ledger.txt ta_lv_vs_cycles.txt; do
  cmp "$O/$f" "$H/outputs/$f"
  echo "identical $f"
done
if [ -n "$RAW" ]; then
  python3 -I "$H/scripts/ta_lv_recheck.py" 0200000000010001 "$RAW"/item3/cycle-*/tap.pcap > "$O/ta_lv_all.txt"
  # The decoder prints each capture's path; compare with the lane's raw root removed.
  sed "s#^$RAW/##" "$O/ta_lv_all.txt" > "$O/ta_lv_all.rel"
  sed "s#^/tmp/608-b14/raw/##" "$H/outputs/ta_lv_all.txt" > "$O/ta_lv_all.ref"
  cmp "$O/ta_lv_all.rel" "$O/ta_lv_all.ref"
  echo "identical ta_lv_all.txt (paths relative to the raw root)"
fi
