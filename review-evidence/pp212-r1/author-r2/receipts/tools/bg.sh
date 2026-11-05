#!/usr/bin/env bash
# bg.sh <outdir> <name> <dir> <command...>: start one gate detached (same unit), keeping cmd/log/rc/start/end
set -u
O=$1; n=$2; d=$3; shift 3
mkdir -p "$O"
rm -f "$O/$n.rc" "$O/$n.end"
echo "$*" > "$O/$n.cmd"
date +%s > "$O/$n.start"
setsid nohup bash -c 'cd "$1" && shift && "$@" > "$0.log" 2>&1; echo $? > "$0.rc"; date +%s > "$0.end"' "$O/$n" "$d" "$@" < /dev/null > /dev/null 2>&1 &
echo "started $n pid $!"
