#!/bin/bash
# job.sh NAME MAKE_JOBS ARGS...: one harness run detached, with its own log and rc file.
P=$REVIEWS/665s2-r703-2-packet
. $P/scripts/env.sh
NAME=$1 MJ=$2; shift 2
export REVIEW_MAKE_JOBS=$MJ
cd $REVIEWS/r703-2-665s2
rm -f $P/scratch/logs/$NAME.rc
/usr/bin/time -v python3 -B tb/verilator/ctrl_service_budget/run.py "$@" > $P/scratch/logs/$NAME.log 2>&1
echo $? > $P/scratch/logs/$NAME.rc
