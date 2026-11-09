#!/bin/bash
# usage: bg.sh <receipt-dir> <name> <workdir> <command...>
# runs the command detached, recording .cmd .start .log .rc .end in <receipt-dir>
set -u
R=$1; N=$2; W=$3; shift 3
mkdir -p "$R"
printf '%s\n' "cd $W && $*" > "$R/$N.cmd"
date +%s > "$R/$N.start"
setsid nohup bash -c 'cd "$1" || exit 99; shift; R=$1; N=$2; shift 2; "$@" > "$R/$N.log" 2>&1; echo $? > "$R/$N.rc"; date +%s > "$R/$N.end"' _ "$W" "$R" "$N" "$@" < /dev/null > /dev/null 2>&1 &
echo "started $N pid $!"
