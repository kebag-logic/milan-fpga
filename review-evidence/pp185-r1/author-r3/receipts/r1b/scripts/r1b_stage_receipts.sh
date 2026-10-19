#!/usr/bin/env bash
# copy the round 1b receipts into the output directory: files <= 200 KB are copied,
# larger ones recorded by sha256 and size in receipts/OVER-200KB.sha256
S=$VALIDATION_STORAGE/pp185-a647/r1b; O=$MANAGEMENT/2026-09-23/pp185-a647/receipts
over="$O/OVER-200KB.sha256"
for d in head parent-head head-campaigns newarms hand try; do
  (cd "$S" && find "$d" -type f ! -path "head-campaigns/out/*") | while read -r f; do
    sz=$(stat -c %s "$S/$f")
    if [ "$sz" -gt 204800 ]; then
      line="$(sha256sum "$S/$f" | cut -d' ' -f1)  $sz  r1b/$f"
      grep -qF "r1b/$f" "$over" || echo "$line" >> "$over"
    else
      mkdir -p "$O/r1b/$(dirname "$f")"; cp -p "$S/$f" "$O/r1b/$f"
    fi
  done
done
cp -p $VALIDATION_STORAGE/pp185-a647/scripts/r1b_*.sh $VALIDATION_STORAGE/pp185-a647/scripts/receipts_index.py "$O/r1b/" 2>/dev/null
mkdir -p "$O/r1b/scripts"; mv "$O"/r1b/r1b_*.sh "$O"/r1b/receipts_index.py "$O/r1b/scripts/"
cp -p $VALIDATION_STORAGE/pp185-a647/scripts/{gate,proc_gates,campaigns2,parent_gates}.sh "$O/r1b/scripts/"
