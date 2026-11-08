#!/bin/sh
# receipt.sh RAW OUT PATTERN COMMAND... : write OUT, a public receipt of RAW.
# Header: the head, the command, the raw log's size and sha256. Body: RAW's lines matching the
# extended regex PATTERN ('.' keeps every line), with local paths replaced by placeholders.
set -eu
RAW=$1; OUT=$2; PAT=$3; shift 3
{
  echo "head e69d243a61a8ec1c1ad8c473f809e1351dab1b61"
  echo "command: $*"
  echo "raw log: $(wc -c < "$RAW") bytes, sha256 $(sha256sum "$RAW" | cut -d' ' -f1) (kept unpublished; lines below filtered by /$PAT/)"
  echo "---"
  grep -E -- "$PAT" "$RAW" | sed -e 's#/home/[^ ]*/overlay/[0-9a-f]*/diff#<pinned-verilator-5.050-root>#g' \
    -e 's#$VALIDATION_TOOLS/pinned-verilator-5.050/verilator#<pinned-verilator-5.050>#g' \
    -e 's#$REVIEWS/665s6b-r800-1-packet#<packet>#g' \
    -e 's#$REVIEWS/r800-1-665s6b#<clone>#g' -e 's#/home/[A-Za-z0-9_]*#<home>#g'
} > "$OUT"
