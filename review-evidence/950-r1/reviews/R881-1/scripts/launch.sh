#!/bin/sh
# launch.sh <receipt-dir> <name> <cmd...>: run cmd detached, its output in <name>.log and its exit status in <name>.rc
set -eu
dir=$1; name=$2; shift 2
mkdir -p "$dir"
( "$@" > "$dir/$name.log" 2>&1; echo $? > "$dir/$name.rc" ) < /dev/null > /dev/null 2>&1 &
echo "launched $name"
