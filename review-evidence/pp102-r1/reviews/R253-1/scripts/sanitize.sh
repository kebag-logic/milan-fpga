#!/bin/sh
# Replace host-specific path prefixes in receipts with neutral placeholders,
# in place. Only these literal prefixes are rewritten; no other byte changes.
#   packet root          -> $PACKET
#   review clone         -> $REVIEW_CLONE
#   scoped tool storage  -> $VALIDATION_STORAGE
#   workspace home       -> $WORKSPACE_HOME
# usage: sanitize.sh PACKET_ROOT REVIEW_CLONE STORAGE_ROOT HOME_ROOT FILE...
set -eu
packet=$1 clone=$2 storage=$3 home=$4; shift 4
for f in "$@"; do
  sed -i -e "s#$packet#\$PACKET#g" -e "s#$clone#\$REVIEW_CLONE#g" \
         -e "s#$storage#\$VALIDATION_STORAGE#g" -e "s#$home#\$WORKSPACE_HOME#g" "$f"
done
