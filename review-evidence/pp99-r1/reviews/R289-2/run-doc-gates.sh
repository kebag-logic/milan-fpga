#!/usr/bin/env bash
# Run the repository's docs-gates commands and the make check target in a clone.
# Usage: run-doc-gates.sh <clone-dir> <receipt-dir>
set -u
cd "$1"; out="$2"; mkdir -p "$out"
echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')" > "$out/gates.txt"
for cmd in "python3 scripts/check-links.py" "python3 scripts/check-matrix.py" \
           "python3 scripts/check-integrator-params.py" \
           "python3 scripts/render-wavedrom.py --check" "make stale" "make check"; do
  $cmd > "$out/tmp.log" 2>&1; rc=$?
  { echo "=== $cmd -> rc=$rc"; tail -n 15 "$out/tmp.log"; } >> "$out/gates.txt"
done
rm -f "$out/tmp.log"
cat "$out/gates.txt"
