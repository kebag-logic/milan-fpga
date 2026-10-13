#!/bin/bash
# usage: run_logged.sh NAME CMD...   -> receipts/NAME.log and receipts/NAME.rc, run from $REPO
. "$(dirname "$0")/env.sh"
name=$1; shift
cd "$REPO" || exit 2
{ echo "# cmd: $*"; echo "# start: $(date -u +%FT%TZ) head: $(git rev-parse HEAD)"; } > "$PACKET/receipts/$name.log"
"$@" >> "$PACKET/receipts/$name.log" 2>&1
rc=$?
echo "# end: $(date -u +%FT%TZ) rc=$rc" >> "$PACKET/receipts/$name.log"
echo $rc > "$PACKET/receipts/$name.rc"
