#!/bin/sh
# usage: bg.sh NAME WORKDIR CMD...   (runs CMD detached; writes receipts/NAME.{log,rc,start,end})
# Environment: PKT (packet root), VERILATOR (pinned wrapper), TMPDIR (scratch temp)
set -u
name=$1; dir=$2; shift 2
r="$PKT/receipts"
date -u +%FT%TZ > "$r/$name.start"
( cd "$dir" && "$@" ) > "$r/$name.log" 2>&1
echo $? > "$r/$name.rc"
date -u +%FT%TZ > "$r/$name.end"
