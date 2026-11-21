#!/bin/sh
# usage: run_job.sh <name> <cmd...>; runs <cmd> from the reviewed clone and writes
# $PACKET/receipts/<name>.log and <name>.rc. PACKET, CLONE and VERILATOR are overridable.
PACKET=${PACKET:-$REVIEWS/948-r877-1-packet}
CLONE=${CLONE:-$REVIEWS/r877-1-948}
name=$1; shift
cd "$CLONE" || exit 2
export VERILATOR=${VERILATOR:-$VALIDATION_TOOLS/pinned-verilator-5.050/verilator}
export PATH="$(dirname "$VERILATOR"):$PATH"
{ echo "# job $name start $(date -u +%FT%TZ) head $(git rev-parse HEAD)"; echo "# cmd: $*"; } > "$PACKET/receipts/$name.log"
"$@" >> "$PACKET/receipts/$name.log" 2>&1
rc=$?
echo "# end $(date -u +%FT%TZ) rc=$rc" >> "$PACKET/receipts/$name.log"
echo $rc > "$PACKET/receipts/$name.rc"
