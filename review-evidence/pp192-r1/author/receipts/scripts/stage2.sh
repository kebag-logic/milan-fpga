#!/usr/bin/env bash
# usage: stage2.sh <src-dir> <dest-subdir> [shallow]   copy a record directory's result files
# into receipts/<dest>, host paths masked. Never copied: a campaign unit's source-tree copy
# (`source/`), build directories (`obj_dir/`, `obj_*/`) and build products (.o .d .a .mk
# .hex .bin .sv .patch). A file over 200 KB after masking is listed in OVER-200KB.sha256
# (sha256, bytes, path) and replaced by `<file>.excerpt.txt`: its FAIL, tally and verdict
# lines, read as text. `shallow`: the top level and one directory below only.
O=<management>
src="${1%/}"; dst="$O/$2"; depth=(); [ "$3" = shallow ] && depth=(-maxdepth 2)
mask() { sed -e 's#<scratch>#<scratch>#g' \
             -e 's#<lane>#<lane>#g' \
             -e 's#<home>/\.local/share/containers/storage/overlay/[0-9a-f]*/diff#<toolroot>#g' \
             -e 's#<management> ]*#<management>#g' \
             -e 's#<home>#<home>#g' -e 's#<data>#<data>#g' "$1"; }
find "$src" "${depth[@]}" -type f \
     -not -path '*/source/*' -not -path '*/obj_dir/*' -not -path '*/obj_*/*' \
     -not -name '*.o' -not -name '*.d' -not -name '*.a' -not -name '*.mk' -not -name '*.hex' \
     -not -name '*.bin' -not -name '*.sv' -not -name '*.patch' -not -name '*.pid' | sort |
while read -r f; do
  rel="${f#$src/}"; out="$dst/$rel"; mkdir -p "$(dirname "$out")"
  tmp=$(mktemp); mask "$f" > "$tmp"
  n=$(stat -c %s "$tmp")
  if [ "$n" -gt 204800 ]; then
    echo "$(sha256sum < "$tmp" | cut -d' ' -f1)  $n  $2/$rel" >> "$O/OVER-200KB.sha256"
    grep -a -n -E '^ *(FAIL|\[FAIL\])|checks|RESULT:|sim_pool:|\[GSI\] G9|make: \*\*\*' "$tmp" \
      | head -c 200000 > "$out.excerpt.txt"
    rm -f "$tmp"
  else
    mv "$tmp" "$out"; chmod 644 "$out"
  fi
done
