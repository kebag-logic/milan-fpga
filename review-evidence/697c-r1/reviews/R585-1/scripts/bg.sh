#!/bin/bash
# bg.sh <name> <dir> <cmd...>: run a command detached with its own log and rc file under $RUNS.
name=$1; dir=$2; shift 2
( cd "$dir" && "$@" ) > "$RUNS/$name.log" 2>&1; echo $? > "$RUNS/$name.rc"
