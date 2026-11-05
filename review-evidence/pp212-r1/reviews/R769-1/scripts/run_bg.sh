#!/usr/bin/env bash
# run_bg.sh <name> <dir> <cmd...>: run cmd in dir, log to receipts/<name>.log, rc to receipts/<name>.rc
P=$REVIEWS/pp212-r769-1-packet
name=$1; dir=$2; shift 2
cd "$dir" || exit 1
export PATH=$P/scratch/bin:$PATH TMPDIR=$P/scratch/tmp
"$@" > "$P/receipts/$name.log" 2>&1
echo $? > "$P/receipts/$name.rc"
