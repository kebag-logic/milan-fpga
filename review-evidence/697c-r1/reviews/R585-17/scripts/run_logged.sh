#!/bin/sh
# run_logged.sh NAME TMPDIR CMD...: run CMD from the current directory with TMPDIR set,
# writing receipts/NAME.log and receipts/NAME.rc (exit status and wall seconds).
P=$(cd "$(dirname "$0")/.." && pwd)
name=$1; tmp=$2; shift 2
mkdir -p "$tmp"
start=$(date +%s)
TMPDIR=$tmp "$@" > "$P/receipts/$name.log" 2>&1
rc=$?
echo "rc=$rc elapsed=$(( $(date +%s) - start ))s" > "$P/receipts/$name.rc"
