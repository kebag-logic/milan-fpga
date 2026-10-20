#!/usr/bin/env bash
# Mask host paths in the packet's receipts in place before publication.
# usage: mask.sh <packet>
set -euo pipefail
P=$1
find "$P/receipts" -type f -print0 | xargs -0 sed -i \
  -e "s#$P/scratch#<scratch>#g" -e "s#$P#<packet>#g" \
  -e "s#$REVIEWS/r675-1-pp192#<clone>#g" \
  -e "s#$WORKSPACE_HOME/.local/share/containers/storage/overlay/[0-9a-f]*/diff#<toolroot>#g" \
  -e "s#$WORKSPACE_HOME#<home>#g" -e "s#$VALIDATION_STORAGE#<data>#g" -e "s#/tmp/[A-Za-z0-9._-]*#<tmp>#g"
