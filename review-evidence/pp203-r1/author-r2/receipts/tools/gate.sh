#!/usr/bin/env bash
# gate.sh <outdir> <name> <dir> <command...>: run one gate in the foreground, keep cmd/log/rc/start/end and memory samples
set -u
O=$1; n=$2; d=$3; shift 3
mkdir -p "$O"
echo "$*" > "$O/$n.cmd"
date +%s > "$O/$n.start"
(cd "$d" && MEMLOG="$O/$n.mem" <tools>/withmem.sh "$@") > "$O/$n.log" 2>&1
echo $? > "$O/$n.rc"
date +%s > "$O/$n.end"
echo "$n rc=$(cat "$O/$n.rc") $(( $(cat "$O/$n.end") - $(cat "$O/$n.start") ))s"
