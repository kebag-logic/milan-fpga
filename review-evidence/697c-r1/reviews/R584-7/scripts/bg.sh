#!/bin/sh
# usage: bg.sh <name> <workdir> <command...>  -> receipts/<name>.log, receipts/<name>.rc
name=$1; dir=$2; shift 2
R="$PACKET/receipts"
( cd "$dir" && { echo "# cwd: (clone) head $(git rev-parse HEAD)"; echo "# cmd: $*"; echo "# start: $(date -u +%FT%TZ)"; } > "$R/$name.log"
  "$@" >> "$R/$name.log" 2>&1; rc=$?; echo "# end: $(date -u +%FT%TZ) rc=$rc" >> "$R/$name.log"; echo $rc > "$R/$name.rc" ) &
