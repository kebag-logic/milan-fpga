#!/usr/bin/env bash
# Render each extracted graph (.mmd) to PNG at native size and at page width.
# Usage: render-png.sh GRAPHDIR OUTDIR [PAGE_WIDTH]
set -u
in=$1; out=$2; pw=${3:-830}; mkdir -p "$out"
ls "$in"/*.mmd | xargs -P 8 -I{} bash -c '
  f={}; b=$(basename "$f" .mmd)
  mmdc -i "$f" -o "'"$out"'/$b.native.png" -b white -w 3000 >/dev/null 2>&1; r1=$?
  mmdc -i "$f" -o "'"$out"'/$b.page'"$pw"'.png" -b white -w '"$pw"' >/dev/null 2>&1; r2=$?
  echo "$b native_rc=$r1 page_rc=$r2"'
