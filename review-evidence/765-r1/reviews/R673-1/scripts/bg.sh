#!/bin/bash
# bg.sh NAME DIR CMD... : run CMD in DIR detached, log to receipts/NAME.log, rc to receipts/NAME.rc
P=${PACKET:-$(cd "$(dirname "$0")/.." && pwd)}
name=$1; dir=$2; shift 2
rm -f "$P/receipts/$name.rc"
setsid nohup bash -c 'cd "$1" || exit 99; shift; name=$1; P=$2; shift 2; export PATH="$P/scratch/bin:$PATH"; start=$(date +%s); "$@" > "$P/receipts/$name.log" 2>&1; rc=$?; echo "rc=$rc wall_s=$(( $(date +%s)-start ))" > "$P/receipts/$name.rc"' _ "$dir" "$name" "$P" "$@" > /dev/null 2>&1 &
echo "started $name"
