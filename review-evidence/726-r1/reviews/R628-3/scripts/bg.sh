#!/bin/sh
# Usage: bg.sh NAME DIR CMD...   Runs CMD in DIR detached; writes receipts/NAME.log and NAME.rc
P=$REVIEWS/726-r628-3-packet
name=$1; dir=$2; shift 2
log=$P/receipts/$name.log; rc=$P/receipts/$name.rc
rm -f "$rc"
( cd "$dir" && export TMPDIR=$P/scratch/tmp VERILATOR=$VALIDATION_TOOLS/pinned-verilator-5.050/verilator && \
  { echo "# cmd: $*"; echo "# dir: $dir"; echo "# start: $(date -u +%FT%TZ)"; } > "$log" && \
  "$@" >> "$log" 2>&1; r=$?; echo "# end: $(date -u +%FT%TZ) rc=$r" >> "$log"; echo $r > "$rc" ) </dev/null >/dev/null 2>&1 &
echo "started $name"
