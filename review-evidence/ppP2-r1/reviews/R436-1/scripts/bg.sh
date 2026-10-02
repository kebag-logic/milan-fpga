#!/usr/bin/env bash
# bg.sh NAME DIR CMD... : run CMD in DIR detached; log to receipts/NAME.log, rc to receipts/NAME.rc
set -u
PKT=$(cd "$(dirname "$0")/.." && pwd)
name=$1; dir=$2; shift 2
rm -f "$PKT/receipts/$name.rc"
( cd "$dir" && { echo "# cmd: $*"; echo "# dir: $dir"; echo "# start: $(date -Is)"; } > "$PKT/receipts/$name.log"
  "$@" >> "$PKT/receipts/$name.log" 2>&1; rc=$?
  echo "# end: $(date -Is) rc=$rc" >> "$PKT/receipts/$name.log"; echo $rc > "$PKT/receipts/$name.rc" ) </dev/null >/dev/null 2>&1 &
disown 2>/dev/null || true
echo "started $name pid $!"
