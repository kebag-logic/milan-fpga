#!/bin/sh
# Make the packet's receipts public-safe and list them in MANIFEST.sha256.
# Replaces the reviewer host's home directory with $HOME in every text
# receipt, then hashes every file under receipts/ and scripts/ (never
# scratch/) relative to the packet root.
set -eu
P=$REVIEWS/gptp104-r840-1-packet
cd "$P"
find receipts -type f | while read -r f; do
  if grep -Iq . "$f" 2>/dev/null; then
    sed -i -e "s|$HOME|\$HOME|g" "$f"
  fi
done
find receipts scripts -type f | sort | xargs sha256sum > MANIFEST.sha256
wc -l MANIFEST.sha256
