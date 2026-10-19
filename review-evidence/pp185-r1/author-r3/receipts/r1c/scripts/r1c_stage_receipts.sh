#!/usr/bin/env bash
# copy the round 1c receipts into the output directory: files <= 200 KB are copied,
# larger ones recorded by sha256 and size in receipts/OVER-200KB.sha256; the campaigns'
# per-mutant logs stay in the scratch records (their failing checks are in compare/)
S=$VALIDATION_STORAGE/pp185-a647/r1c; O=$MANAGEMENT/2026-09-23/pp185-a647/receipts
over="$O/OVER-200KB.sha256"
for d in base head head-final parent-base parent-head compare try; do
  [ -d "$S/$d" ] || continue
  (cd "$S" && find "$d" -type f ! -path "*/campaigns/out/*") | while read -r f; do
    sz=$(stat -c %s "$S/$f")
    if [ "$sz" -gt 204800 ]; then
      line="$(sha256sum "$S/$f" | cut -d' ' -f1)  $sz  r1c/$f"
      grep -qF "r1c/$f" "$over" || echo "$line" >> "$over"
    else
      mkdir -p "$O/r1c/$(dirname "$f")"; cp -p "$S/$f" "$O/r1c/$f"
    fi
  done
done
mkdir -p "$O/r1c/scripts"
cp -p $VALIDATION_STORAGE/pp185-a647/scripts/r1c_*.sh $VALIDATION_STORAGE/pp185-a647/scripts/r1c_*.py \
      $VALIDATION_STORAGE/pp185-a647/scripts/{gate,proc_gates,campaigns2,parent_gates,wait}.sh \
      $VALIDATION_STORAGE/pp185-a647/scripts/{receipts_index,anchor_check}.py "$O/r1c/scripts/"
