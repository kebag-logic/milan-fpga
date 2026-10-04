#!/bin/sh
# bg.sh NAME DIR CMD... : run CMD in DIR detached, log to receipts/NAME.log, rc to receipts/NAME.rc
PKT=$REVIEWS/pp639-r462-3-packet
name=$1; dir=$2; shift 2
rm -f "$PKT/receipts/$name.rc"
( cd "$dir" && { echo "# $(date -Is) cwd=$dir cmd=$*"; "$@"; } > "$PKT/receipts/$name.log" 2>&1; echo $? > "$PKT/receipts/$name.rc" ) &
