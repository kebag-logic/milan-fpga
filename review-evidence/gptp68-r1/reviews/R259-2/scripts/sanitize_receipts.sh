#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Replace host paths in receipts with the placeholders env.sh defines.
set -eu
. "$(dirname "$0")/env.sh"
for f in "$RECEIPTS"/*; do
  sed -i -e "s|$PACKET|\$PACKET|g" -e "s|$CLONE|\$CLONE|g" -e "s|$PIN_BIN|\$PIN_BIN|g" \
         -e "s|/home/[a-z]*/.local/share/containers/storage/overlay/[0-9a-f]*/diff|\$PINNED_ROOT|g" \
         -e "s|/home/[a-z]*|\$HOME|g" -e "s|$VALIDATION_STORAGE|\$DATA|g" "$f"
done
