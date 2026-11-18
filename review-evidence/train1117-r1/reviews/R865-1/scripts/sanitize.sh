#!/bin/bash
# Replace host-local paths in the packet's text receipts with neutral placeholders, in place.
# usage: CLONE=<reviewed clone> sanitize.sh <packet dir> <file...>
packet=$1; shift
for f in "$@"; do
  [ -f "$f" ] || continue
  sed -i -e "s#$packet/scratch#<scratch>#g" -e "s#$packet#<packet>#g" \
         ${CLONE:+-e "s#$CLONE#<clone>#g"} \
         -e "s#$VALIDATION_TOOLS#<tools>#g" -e "s#$HOME#<home>#g" -e "s#/tmp/#<tmp>/#g" "$f"
done
