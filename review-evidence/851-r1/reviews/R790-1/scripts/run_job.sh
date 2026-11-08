#!/usr/bin/env bash
# run_job.sh NAME DIR CMD... : run CMD in DIR, write receipts/NAME.log and receipts/NAME.rc
set -u
name=$1; dir=$2; shift 2
out="$(cd "$(dirname "$0")/.." && pwd)/receipts"
start=$(date -u +%FT%TZ)
( cd "$dir" && "$@" ) > "$out/$name.log" 2>&1
rc=$?
echo "$rc" > "$out/$name.rc"
echo "start $start end $(date -u +%FT%TZ) rc $rc cmd: $*" > "$out/$name.meta"
