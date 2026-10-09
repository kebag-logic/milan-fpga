#!/usr/bin/env bash
# Usage: bg.sh NAME WORKDIR CMD...   runs CMD detached; writes receipts/NAME.log and receipts/NAME.rc
set -u
P=$REVIEWS/pp168-r552-1-packet
name=$1; wd=$2; shift 2
export PATH=$P/scratch/bin:$PATH TMPDIR=$P/scratch/tmp
rm -f "$P/receipts/$name.rc"
( cd "$wd" && { echo "# cmd: $*"; echo "# cwd: $wd"; echo "# start: $(date -Is)"; verilator --version; "$@"; rc=$?; echo "# end: $(date -Is) rc=$rc"; echo $rc > "$P/receipts/$name.rc.tmp"; mv "$P/receipts/$name.rc.tmp" "$P/receipts/$name.rc"; } ) > "$P/receipts/$name.log" 2>&1 < /dev/null &
disown
echo "started $name pid $!"
