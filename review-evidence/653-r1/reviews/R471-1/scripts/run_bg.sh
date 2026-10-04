#!/bin/sh
# run_bg.sh NAME DIR CMD...  - run CMD in DIR detached; log to receipts/NAME.log, rc to receipts/NAME.rc
P=$(cd "$(dirname "$0")/.." && pwd)
name=$1; dir=$2; shift 2
rm -f "$P/receipts/$name.rc"
( cd "$dir" && { date -u +"start %FT%TZ"; echo "+ $*"; "$@"; rc=$?; date -u +"end %FT%TZ"; echo "rc=$rc"; echo $rc > "$P/receipts/$name.rc"; } ) > "$P/receipts/$name.log" 2>&1 &
