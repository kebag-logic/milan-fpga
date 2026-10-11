#!/bin/sh
# Replace host, home and packet paths in receipts with neutral placeholders
# before publication. The unsanitized originals are kept under scratch/.
#   usage: sanitize_receipts.sh PACKET
set -eu
P=$1
mkdir -p "$P/scratch/receipts-raw"
cp -a "$P/receipts/." "$P/scratch/receipts-raw/"
find "$P/receipts" -type f | while read -r f; do
  sed -i -E \
    -e "s#$P#<packet>#g" \
    -e "s#/home/[A-Za-z0-9_.-]+#<home>#g" \
    -e "s#$REVIEWS/r615-1-g70#<clone>#g" \
    -e "s#$VALIDATION_TOOLS/[A-Za-z0-9_.-]+#<tools>#g" \
    -e "s#(Running On[ ]*: )[^ |]+#\1<host>#g" \
    -e "s#(Host[ ]*: )[A-Za-z0-9_.-]+#\1<host>#g" \
    -e "s#(Host memory[ ]*: )[0-9]+ MB#\1<mem>#g" \
    "$f"
done
grep -rl -E "/home/|$(uname -n)|$(id -un)" "$P/receipts" && { echo "residual identifiers"; exit 1; } || echo "sanitized"
