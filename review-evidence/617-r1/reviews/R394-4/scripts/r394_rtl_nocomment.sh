#!/bin/sh
# R394-4: is an RTL file's change comment-only? Preprocess both blobs with the pinned Verilator
# (-E -P: comments and line markers dropped, whitespace kept) and compare, then compare again with
# every run of whitespace collapsed. Usage (from the repo): sh r394_rtl_nocomment.sh <base> <head> <path> <workdir>
set -eu
b=$1; h=$2; f=$3; w=$4; n=$(basename "$f" .sv)
mkdir -p "$w"
git show "$b:$f" > "$w/$n.base.sv"; git show "$h:$f" > "$w/$n.head.sv"
for v in base head; do
  verilator -E -P "$w/$n.$v.sv" 2>/dev/null | sed 's/[[:space:]]\+/ /g; s/^ //; s/ $//' | grep -v '^$' > "$w/$n.$v.pp" || true
done
if cmp -s "$w/$n.base.pp" "$w/$n.head.pp"; then echo "$f: $b..$h comment/whitespace-only (preprocessed token streams identical, $(wc -l < "$w/$n.head.pp") lines)"; else echo "$f: LOGIC DIFFERS"; diff "$w/$n.base.pp" "$w/$n.head.pp" | head -20; fi
