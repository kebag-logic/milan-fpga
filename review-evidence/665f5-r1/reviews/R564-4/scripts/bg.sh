#!/bin/bash
# bg.sh NAME LOGDIR CMD... : run CMD detached, log to LOGDIR/NAME.log, rc to LOGDIR/NAME.rc
name=$1; dir=$2; shift 2
rm -f "$dir/$name.rc"
setsid nohup bash -c '"$@" > "'"$dir/$name.log"'" 2>&1; echo $? > "'"$dir/$name.rc"'"' _ "$@" < /dev/null > /dev/null 2>&1 &
