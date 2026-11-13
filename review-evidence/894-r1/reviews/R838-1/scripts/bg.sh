#!/bin/bash
# usage: bg.sh <log-dir> <name> <cmd...>: run cmd, its output to <name>.log and its exit status to <name>.rc
d=$1; n=$2; shift 2; "$@" > "$d/$n.log" 2>&1; echo $? > "$d/$n.rc"
