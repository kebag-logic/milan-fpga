#!/usr/bin/env bash
# usage: stage.sh <src-dir> <dest-subdir>   copy every file into receipts/<dest>, host
# paths masked; a file over 200 KB after masking is listed in OVER-200KB.sha256 instead
O=<management>
src="${1%/}"; dst="$O/$2"; mkdir -p "$dst"
mask() { sed -e 's#<scratch>#<scratch>#g' \
             -e 's#<lane>#<lane>#g' \
             -e 's#<home>/\.local/share/containers/storage/overlay/[0-9a-f]*/diff#<toolroot>#g' \
             -e 's#<management> ]*#<management>#g' \
             -e 's#<home>#<home>#g' -e 's#<data>#<data>#g' "$1"; }
find "$src" -type f | sort | while read -r f; do
  rel="${f#$src/}"; out="$dst/$rel"; mkdir -p "$(dirname "$out")"
  tmp=$(mktemp); mask "$f" > "$tmp"
  n=$(stat -c %s "$tmp")
  if [ "$n" -gt 204800 ]; then
    echo "$(sha256sum < "$tmp" | cut -d' ' -f1)  $n  $2/$rel" >> "$O/OVER-200KB.sha256"
    # keep the verdict: its FAIL lines and tally, as an excerpt beside the listing
    grep -E '^FAIL|checks' "$tmp" | head -c 200000 > "$out.fails.txt"; rm -f "$tmp"
  else
    mv "$tmp" "$out"; chmod 644 "$out"
  fi
done
