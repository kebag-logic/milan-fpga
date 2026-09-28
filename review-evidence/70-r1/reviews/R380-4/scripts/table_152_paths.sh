#!/bin/sh
# List D3 section 15.2 table rows' processor paths and check each exists at the
# pinned processor commit. Run from the parent repository root.
set -u
D3=docs/design/SAVED_STATE_MATERIALIZATION.md
PIN=16be6768f710e79450aace277abacd6c2c3336e5
awk '/^### 15\.2/{f=1;next} f&&/^## 16\./{exit} f' "$D3" | grep -E '^\| \[' > /tmp/r380_2_rows_$$.txt
echo "rows: $(wc -l < /tmp/r380_2_rows_$$.txt)"
sed -E 's/^\| \[([^]]+)\].*/\1/' /tmp/r380_2_rows_$$.txt | sort | uniq -c > /tmp/r380_2_files_$$.txt
echo "distinct files: $(wc -l < /tmp/r380_2_files_$$.txt)"
while read -r n f; do
  if git -C protocol-processor cat-file -e "$PIN:$f" 2>/dev/null; then s=EXISTS; else s=MISSING; fi
  printf '%s %s %s\n' "$n" "$f" "$s"
done < /tmp/r380_2_files_$$.txt
echo "## link targets pinned to $PIN:"
grep -o -E 'blob/[0-9a-f]{40}/' /tmp/r380_2_rows_$$.txt | sort | uniq -c
rm -f /tmp/r380_2_rows_$$.txt /tmp/r380_2_files_$$.txt
