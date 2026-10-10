#!/bin/sh
# run_bg.sh NAME DIR CMD... : run CMD in DIR; log to $PACKET/receipts/NAME.log
# and the exit status to $PACKET/receipts/NAME.rc. PACKET defaults to this
# script's packet directory.
PACKET=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
name=$1; dir=$2; shift 2
( cd "$dir" && { echo "# cwd: $dir"; echo "# cmd: $*"; echo "# start: $(date -u +%FT%TZ)"; "$@"; rc=$?; echo "# end: $(date -u +%FT%TZ) rc=$rc"; echo $rc > "$PACKET/receipts/$name.rc"; } ) > "$PACKET/receipts/$name.log" 2>&1
