#!/usr/bin/env bash
# #787 round 2: copy one finished bank's receipts into the output directory through collect.py (host paths replaced,
# files over 200 KB recorded by size and SHA-256 instead).
# usage: collect_bank.sh <source-dir> <receipt-subdir>
set -eu
D=$(cd "$(dirname "$0")" && pwd)
src=$1; dest=$(dirname "$D")/receipts/$2
mkdir -p "$dest"
find "$src" -type f | sort | while read -r f; do
  rel=${f#"$src"/}
  mkdir -p "$dest/$(dirname "$rel")"
  python3 "$D/collect.py" "$dest/$(dirname "$rel")" "$f" "$(basename "$rel")" > /dev/null
done
echo "collected $(find "$dest" -type f | wc -l) files into receipts/$2"
