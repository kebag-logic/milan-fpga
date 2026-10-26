#!/bin/sh
# launch_root.sh ROOT NAME ARGS... : run ROOT's harness copy detached with its own log and rc file.
P=$REVIEWS/665s2-r703-1-packet
. $P/scripts/env.sh
R=$1; NAME=$2; shift 2
cd $R
( /usr/bin/time -v python3 -B tb/verilator/ctrl_service_budget/run.py "$@" > $P/scratch/logs/$NAME.log 2>&1; echo $? > $P/scratch/logs/$NAME.rc ) &
