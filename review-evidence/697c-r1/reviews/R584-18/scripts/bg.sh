#!/usr/bin/env bash
# bg.sh <name> <dir> <cmd...>: run a command detached in <dir>, log to receipts/<name>.log, rc to receipts/<name>.rc
set -u
name=$1; dir=$2; shift 2
R="$PACKET/receipts"; mkdir -p "$R"; rm -f "$R/$name.rc"
( cd "$dir" && { echo "# cwd: $dir"; echo "# cmd: $*"; echo "# start: $(date -u +%FT%TZ)"; } > "$R/$name.log"
  start=$(date +%s); "$@" >> "$R/$name.log" 2>&1; rc=$?
  echo "# end: $(date -u +%FT%TZ) elapsed=$(( $(date +%s) - start ))s rc=$rc" >> "$R/$name.log"; echo $rc > "$R/$name.rc" ) &
