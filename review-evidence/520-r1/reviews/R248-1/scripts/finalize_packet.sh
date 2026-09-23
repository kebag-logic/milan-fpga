#!/usr/bin/env bash
# Copy probe receipts into receipts/, neutralise host paths, refuse leaks,
# and write MANIFEST.sha256 (paths relative to the packet root).
# usage: finalize_packet.sh PACKET_ROOT CLONE_ROOT
set -euo pipefail
root="$1"; clone="$2"
cd "$root"
for w in gptp ltn ucode; do
  src="scratch/probe-work-$w"
  [ -d "$src" ] || continue
  for f in "$src"/probe-*.json "$src"/driver.log; do
    [ -f "$f" ] || continue
    cp "$f" "receipts/real-probe-$w-$(basename "$f")"
  done
done
# neutralise absolute host paths in every receipt
for f in receipts/*; do
  sed -i -e "s#$root/scratch/[^ \"',]*/<work>#<work>#g" -e "s#$root#<packet>#g" \
         -e "s#$clone#<clone>#g" -e "s#$HOME#<home>#g" "$f"
done
# leak patterns are assembled so this file does not match itself
leak_re="/da""ta/|/ho""me/|/tm""p/cl"
if grep -rqE "$leak_re" receipts scripts REPORT.md; then
  grep -rnE "$leak_re" receipts scripts REPORT.md | head >&2
  echo "path leak found; refusing to write the manifest" >&2
  exit 1
fi
find receipts scripts -type f ! -name '*.pyc' | LC_ALL=C sort | xargs sha256sum > MANIFEST.sha256
sha256sum -c MANIFEST.sha256 >/dev/null
echo "manifest entries: $(wc -l < MANIFEST.sha256)"
