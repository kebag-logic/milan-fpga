#!/bin/sh
# Usage: merge_check_probe.sh <repo> <workdir>; shows the hunk-set comparison in merge_reconstruct.sh detects a dropped lane hunk and a dropped dev hunk
set -eu
R=$1; W=$2; cd "$R"
B=c6bd08c6f52632c6d33d834ce842ac3cf63f29cc; L=26e2748f47b0d8fa533f53203264d9f31fc13c48; D=e81ce82f9aa3e4dcaffa5bcdf7e60f0c7cffd80c; M=313616d1a18549d41907db389d378f0beb9bc543
f=docs/design/AREA_BUDGET.md
h(){ grep -E '^[+-][^+-]' | sed 's/^\(.\).*/&/' | sha256sum | cut -c1-16; }
git show $D:$f > "$W/dev.md"; git show $M:$f > "$W/merged.md"
lane=$(git diff -U0 $B $L -- $f | grep -E '^[+-][^+-]' | sha256sum | cut -c1-16)
devh=$(git diff -U0 $B $D -- $f | grep -E '^[+-][^+-]' | sha256sum | cut -c1-16)
# plant 1: drop one lane line (restore the base's gate-record sentence)
sed 's/^All four measurements use the same recipe identity and policy\.$/Both measurements use the same recipe identity and policy./' "$W/merged.md" > "$W/p1.md"
# plant 2: drop one dev line (restore the base's 50-tile budget sentence)
sed 's|^The \[ruling\](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6101485877) binds it: up to 56 RAMB36 as mapped; M8a-1 maps 54 at the largest shape\.$|Budget about 50 RAMB36 tiles for the complete firmware allocation.|' "$W/merged.md" > "$W/p2.md"
git show $L:$f > "$W/lane.md"
for p in merged p1 p2; do
  ov=$(git diff --no-index -U0 "$W/dev.md" "$W/$p.md" | grep -E '^[+-][^+-]' | sha256sum | cut -c1-16 || true)
  ol=$(git diff --no-index -U0 "$W/lane.md" "$W/$p.md" | grep -E '^[+-][^+-]' | sha256sum | cut -c1-16 || true)
  echo "$p: lane-hunks-preserved=$([ "$ov" = "$lane" ] && echo yes || echo NO) dev-hunks-preserved=$([ "$ol" = "$devh" ] && echo yes || echo NO)"
done
cmp -s "$W/merged.md" "$W/p1.md" && echo "p1 plant did not apply" || echo "p1 plant applied"
cmp -s "$W/merged.md" "$W/p2.md" && echo "p2 plant did not apply" || echo "p2 plant applied"
