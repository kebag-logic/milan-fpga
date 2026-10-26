#!/bin/sh
# launch.sh NAME ARGS... : run the harness detached with its own log and rc file.
P=$REVIEWS/665s2-r703-1-packet
. $P/scripts/env.sh
NAME=$1; shift
cd $REVIEWS/r703-1-665s2
( /usr/bin/time -v python3 -B tb/verilator/ctrl_service_budget/run.py "$@" > $P/scratch/logs/$NAME.log 2>&1; echo $? > $P/scratch/logs/$NAME.rc ) &
