#!/usr/bin/env bash
# bg.sh <runs> <name> <dir> <path> <command...>: start one gate detached in this unit (cmd/log/rc/start/end)
set -u
R=$1; n=$2; d=$3; p=$4; shift 4
mkdir -p "$R"; rm -f "$R/$n.rc" "$R/$n.end"
echo "$*" > "$R/$n.cmd"; date +%s > "$R/$n.start"
setsid nohup bash -c 'o=$1; d=$2; p=$3; shift 3; (cd "$d" && PATH="$p" "$@") > "$o.log" 2>&1; echo $? > "$o.rc"; date +%s > "$o.end"' _ "$R/$n" "$d" "$p" "$@" < /dev/null > /dev/null 2>&1 &
echo "started $n pid $!"
