#!/bin/bash
# run.sh <name> <dir> <command...>: run a command in <dir> with the pinned env, log to receipts/<name>.log, rc to .rc
P=$REVIEWS/929-r855-1-packet
name=$1; dir=$2; shift 2
. $P/scripts/env.sh
cd "$dir" || exit 9
log=$P/receipts/$name.log
{ echo "# head $(git rev-parse HEAD) dirty $(git status --porcelain | wc -l) start $(date -Is)"; echo "# cmd: $*"; } > $log
start=$(date +%s)
bash -c "$*" >> $log 2>&1; rc=$?
echo "# end $(date -Is) rc=$rc $(( $(date +%s)-start ))s porcelain-after $(git status --porcelain --untracked-files=no | wc -l)" >> $log
echo $rc > $P/receipts/$name.rc
