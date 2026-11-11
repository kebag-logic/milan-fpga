#!/bin/bash
# bg.sh <name> <cmd...>: run detached in the current directory; log to <scratch>/bg/<name>.log, rc to <name>.rc
d=<scratch>/bg; mkdir -p $d; n=$1; shift
rm -f $d/$n.rc
setsid nohup bash -c '"$@" > "'$d/$n'.log" 2>&1; echo $? > "'$d/$n'.rc"' _ "$@" > /dev/null 2>&1 &
echo started $n
