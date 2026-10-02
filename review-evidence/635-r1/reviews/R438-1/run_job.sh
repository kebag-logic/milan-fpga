#!/bin/bash
# run_job.sh <name> <command...>: run in the review clone, log to logs/<name>.log, rc to logs/<name>.rc
P=$REVIEWS/635-r438-1-packet
name=$1; shift
cd $REVIEWS/r438-1-635 || exit 99
export PATH=$P/scratch/bin:$PATH
{ echo "# $(date -Is) cwd=$PWD cmd: $*"; bash -c "$*"; } > "$P/logs/$name.log" 2>&1
echo $? > "$P/logs/$name.rc"
