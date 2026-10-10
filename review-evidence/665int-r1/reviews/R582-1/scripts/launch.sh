#!/usr/bin/env bash
# launch.sh NAME DIR CMD... : run CMD detached in DIR, log to receipts/NAME.log, exit code to receipts/NAME.rc
set -u
name=$1; dir=$2; shift 2
R="$(cd "$(dirname "$0")/.." && pwd)/receipts"
rm -f "$R/$name.rc"
( cd "$dir" && { echo "# cmd: $*"; echo "# dir: $dir"; echo "# start: $(date -u +%FT%TZ)"; "$@"; rc=$?; echo "# end: $(date -u +%FT%TZ) rc=$rc"; echo $rc > "$R/$name.rc"; } ) > "$R/$name.log" 2>&1 < /dev/null &
disown
echo "launched $name pid $!"
