#!/bin/sh
# Start one named job detached, with its own log and rc file.
# usage: launch.sh NAME DIR CMD...   (PKT defaults to this script's packet)
# Writes receipts/NAME.log and receipts/NAME.rc (rc file appears on exit).
set -u
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
name=$1; dir=$2; shift 2
export PATH="$PKT/bin:$PATH"
export TMPDIR="$PKT/scratch/tmp"
rm -f "$PKT/receipts/$name.rc"
( cd "$dir" && { date -u +"start %FT%TZ"; verilator --version; "$@"; } \
    > "$PKT/receipts/$name.log" 2>&1; echo $? > "$PKT/receipts/$name.rc" ) \
  < /dev/null > /dev/null 2>&1 &
echo "launched $name pid $!"
