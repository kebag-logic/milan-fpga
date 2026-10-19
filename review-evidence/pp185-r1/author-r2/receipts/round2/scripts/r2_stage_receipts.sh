#!/usr/bin/env bash
# copy the round 2 receipts into the output directory: files <= 200 KB are copied,
# larger ones recorded by sha256 and size in receipts/OVER-200KB.sha256 (the campaigns'
# per-mutant logs excepted, see below); then the
# index is regenerated from the files present
S=<data>/tmp/pp185-a647; R="$S/r2/rec"; O=<home>/milan-fpga-management/2026-09-23/pp185-a647/receipts
over="$O/OVER-200KB.sha256"
for d in base head head-final head-final2 parent-base parent-base-stopped-at-xvlog parent-head parent-head-7368215-stopped compare try newarms probes-head labels; do
  [ -d "$R/$d" ] || continue
  # the campaigns' per-mutant logs stay in the scratch records (their failing checks
  # are in compare/); each campaign's results.json is kept
  (cd "$R" && find "$d" -type f \( ! -path "*/campaigns/out/*" -o -name results.json \)) | while read -r f; do
    sz=$(stat -c %s "$R/$f")
    if [ "$sz" -gt 204800 ]; then
      line="$(sha256sum "$R/$f" | cut -d' ' -f1)  $sz  round2/$f"
      grep -qF "round2/$f" "$over" || echo "$line" >> "$over"
    else
      mkdir -p "$O/round2/$(dirname "$f")"; cp -p "$R/$f" "$O/round2/$f"
    fi
  done
done
for f in final-head.txt parent-base.out parent-head.out posting.txt; do
  [ -e "$R/$f" ] && cp -p "$R/$f" "$O/round2/$f"
done
mkdir -p "$O/round2/scripts"
cp -p "$S"/scripts/r2_*.sh "$S"/scripts/r2_*.py \
      "$S"/scripts/{gate,proc_gates,campaigns2,parent_gates,wait,r1c_parent,r1c_parent_head}.sh \
      "$S"/scripts/{receipts_index,anchor_check,r1c_failsets}.py "$O/round2/scripts/"
python3 -I "$S/scripts/receipts_index.py" "$O"
