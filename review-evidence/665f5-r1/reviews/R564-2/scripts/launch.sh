#!/usr/bin/env bash
# Start one named job detached, with its own log and rc file under RECEIPTS.
# Usage: launch.sh <receipts-dir> <name> <cwd> <command...>
set -u
receipts=$1; name=$2; cwd=$3; shift 3
mkdir -p "$receipts"
rm -f "$receipts/$name.rc"
setsid nohup bash -c 'cd "$1" || exit 99; shift; name=$1; receipts=$2; shift 2;
  { echo "command: $*"; echo "start: $(date -u +%FT%TZ)"; } > "$receipts/$name.log"
  "$@" >> "$receipts/$name.log" 2>&1; rc=$?
  echo "end: $(date -u +%FT%TZ) rc=$rc" >> "$receipts/$name.log"; echo $rc > "$receipts/$name.rc"' \
  _ "$cwd" "$name" "$receipts" "$@" < /dev/null > /dev/null 2>&1 &
echo "launched $name"
