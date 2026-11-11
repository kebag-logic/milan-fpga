#!/bin/bash
# bg.sh <name> <logdir> <cwd> <cmd...>: run cmd detached, log to <logdir>/<name>.log, rc to <logdir>/<name>.rc
name=$1 dir=$2 cwd=$3; shift 3
( cd "$cwd" && /usr/bin/time -v "$@" ) > "$dir/$name.log" 2>&1; echo $? > "$dir/$name.rc"
