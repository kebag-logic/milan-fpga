#!/bin/sh
# Compare every Markdown table line of the B6 page between round 1 and round 2,
# and count tables (runs of consecutive '|' lines) on each side.
# Usage: table_identity.sh <repo> <r1-sha> <r2-sha>
set -u
repo=$1; r1=$2; r2=$3
f=docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md
t=$(mktemp -d)
git -C "$repo" show "$r1:$f" > "$t/r1.md"
git -C "$repo" show "$r2:$f" > "$t/r2.md"
for s in r1 r2; do
  grep '^|' "$t/$s.md" > "$t/$s-tables.txt"
  n=$(awk '/^\|/{if(!t){c++;t=1}} !/^\|/{t=0} END{print c}' "$t/$s.md")
  echo "$s: table lines $(wc -l < "$t/$s-tables.txt"), bytes $(wc -c < "$t/$s-tables.txt"), tables $n, sha256 $(sha256sum < "$t/$s-tables.txt" | cut -c1-64)"
done
# Also compare each table with the line that introduces it (the preceding non-table line), so a
# table moved under a different heading or comment marker would show.
for s in r1 r2; do
  awk 'prev!~/^\|/ && /^\|/{print "@@ " last} /^\|/{print} {if($0!~/^\|/ && $0!="") last=$0; prev=$0}' "$t/$s.md" > "$t/$s-ctx.txt"
done
cmp "$t/r1-tables.txt" "$t/r2-tables.txt"; echo "cmp table lines rc=$?"
diff "$t/r1-ctx.txt" "$t/r2-ctx.txt"; echo "diff tables-with-lead-line rc=$?"
rm -rf "$t"
