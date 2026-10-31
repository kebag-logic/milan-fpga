#!/usr/bin/env bash
# Regenerate the CDC census at a checkout into a scratch directory and compare
# the SVG, drawio and (re-rendered per the generator's usage line) PNG with the
# tracked copies.  Usage: check_census.sh <repo-checkout> <scratch-dir>
set -u
REPO=$1; OUT=$2
mkdir -p "$OUT"
python3 -I "$REPO/docs/diagrams/cdc_census.gen.py" "$OUT/cdc_census" || exit 2
rsvg-convert -w 1900 "$OUT/cdc_census.svg" -o "$OUT/cdc_census.png" || exit 2
rc=0
for ext in svg drawio png; do
  if cmp -s "$OUT/cdc_census.$ext" "$REPO/docs/diagrams/cdc_census.$ext"; then
    echo "$ext=equal"
  else
    echo "$ext=DIFFERS"; rc=1
  fi
done
grep -o 'x[0-9]* call sites' "$OUT/cdc_census.svg"
grep -c 'MultiReg(' "$REPO/sw/litex/milan_soc.py" | sed 's/^/MultiReg( call sites in milan_soc.py: /'
exit $rc
