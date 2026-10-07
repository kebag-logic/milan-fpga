#!/bin/sh
# usage: bg.sh <name> <logdir> <cmd...>; writes <name>.log and <name>.rc
n=$1; d=$2; shift 2
( "$@" > "$d/$n.log" 2>&1; echo $? > "$d/$n.rc" ) &
