#!/usr/bin/env bash
# listing.sh OUTDIR: partial-clone the evidence commit, write its complete
# recursive listing (no pager, no truncation) and the census-format listing,
# then run the census and the manifest check against the sparse checkout.
set -euo pipefail
OUT=$(realpath "$1"); HERE=$(cd "$(dirname "$0")" && pwd)
C=ea450d8d30779e24e9dc8588957623e57dbccf48; SUB=review-evidence/pp217-r1
W="$OUT/scratch/ev"; mkdir -p "$W" "$OUT/receipts"; cd "$W"
[ -d .git ] || { git init -q .; git remote add origin https://github.com/kebag-logic/milan-fpga.git; }
git fetch -q --depth 1 --filter=blob:none origin "$C"
git sparse-checkout set --no-cone "/$SUB/" >/dev/null; git checkout -q --detach "$C"
git ls-tree -r --full-tree "$C" > "$OUT/receipts/ea450d8d_ls-tree-r_full.txt"
git ls-tree -r "$C" -- "$SUB" > "$OUT/receipts/ea450d8d_ls-tree-r_pp217-r1.txt"
git ls-tree -r -t -l "$C" -- "$SUB" > "$OUT/receipts/ea450d8d_ls-tree-r-t-l_pp217-r1.txt"
awk -F'\t' '{split($1,a," "); t=(a[2]=="tree")?"tree":"blob"; s=(t=="tree")?"-":a[4]; print t" "s" "$2}' \
  "$OUT/receipts/ea450d8d_ls-tree-r-t-l_pp217-r1.txt" > "$OUT/receipts/ea450d8d_listing_census_format.txt"
wc -l "$OUT"/receipts/ea450d8d_*.txt
python3 -I "$HERE/evidence_census.py" "$OUT/receipts/ea450d8d_listing_census_format.txt" "$W" "$SUB"
python3 -I "$HERE/manifest_check.py" "$W/$SUB"
