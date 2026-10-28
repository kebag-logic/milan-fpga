#!/bin/bash
# Replace host-specific paths in publishable receipts, then write MANIFEST.sha256
# (paths relative to the packet). usage: sanitize_and_manifest.sh <packet>
set -euo pipefail
p="$1"; cd "$p"
find receipts scripts -type f ! -name sanitize_and_manifest.sh -print0 | xargs -0 sed -i \
  -e "s#$p#<packet>#g" \
  -e "s#$REVIEWS/r721-1-gptp88#<review-clone>#g" \
  -e "s#$VALIDATION_TOOLS#<tools>#g" \
  -e "s#/home/[a-z]*/\.local/share/containers/storage/overlay/[0-9a-f]*/diff#<verilator-5.050-root>#g" \
  -e "s#/home/[a-z]*#<home>#g" \
  -e "s#/tmp/[A-Za-z0-9._-]*#<tmp>#g"
find receipts scripts -type f | LC_ALL=C sort | xargs sha256sum > MANIFEST.sha256
