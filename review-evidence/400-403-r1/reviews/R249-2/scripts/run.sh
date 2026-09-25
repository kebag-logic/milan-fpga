#!/bin/sh
# Usage: run.sh <receipt-name> <workdir> <command...>
# Runs one probe in the foreground, writes <name>.log and <name>.exit.
set -u
name=$1; dir=$2; shift 2
out="$(dirname "$0")/../receipts"
start=$(date -u +%FT%TZ)
( cd "$dir" && "$@" ) > "$out/$name.log" 2>&1
rc=$?
printf '%s\n' "cmd: $*" "dir: $dir" "start: $start" "end: $(date -u +%FT%TZ)" "exit: $rc" > "$out/$name.exit"
echo "$name exit=$rc"
