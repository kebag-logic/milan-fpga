#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# finalize.sh : redact local paths in the receipts and write MANIFEST.sha256 over
# scripts/ and receipts/ (paths relative to the packet; scratch/ is never listed).
# The local roots are assembled at run time so this file does not spell them.
set -eu
P=$(cd "$(dirname "$0")/.." && pwd)
cd "$P"
root=$(printf '/%s/%s' data milan)
home=$(printf '/%s/' home)
for f in receipts/*; do
  [ -f "$f" ] || continue
  sed -i -e "s#$P#<packet>#g" \
         -e "s#$root/reviews/r453-1-pp232#<review-clone>#g" \
         -e "s#$root/tools/pinned-verilator-5.050#<pinned-verilator-5.050>#g" \
         -e "s#$home[A-Za-z0-9_.-]*/#\$HOME/#g" "$f"
done
if grep -rlE "$home|$root" receipts scripts REPORT.md; then
  echo "unredacted local path left" >&2
  exit 1
fi
find scripts receipts -type f | LC_ALL=C sort | xargs sha256sum > MANIFEST.sha256
sha256sum -c MANIFEST.sha256 > /dev/null
wc -l < MANIFEST.sha256
