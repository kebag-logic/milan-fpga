#!/usr/bin/env bash
# Write MANIFEST.sha256 (sha256sum format, paths relative to the packet) over
# every publishable receipt and script. REPORT.md is published alongside and
# is deliberately not listed; scratch/ is never published.
# usage: make_manifest.sh <packet-dir>
set -euo pipefail
cd "$1"
find receipts scripts -type f -print0 | sort -z | xargs -0 sha256sum > MANIFEST.sha256
sha256sum -c --quiet MANIFEST.sha256
echo "manifest entries: $(wc -l < MANIFEST.sha256)"
