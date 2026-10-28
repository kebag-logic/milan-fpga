#!/bin/sh
# rungate.sh <logdir> <name> <workdir> <command...>: run one gate, keep its log, rc and seconds.
d=$1; n=$2; w=$3; shift 3
mkdir -p "$d"
s=$(date +%s)
( cd "$w" && "$@" ) > "$d/$n.log" 2>&1
rc=$?
e=$(date +%s)
echo "$rc" > "$d/$n.rc"
echo "$n rc=$rc seconds=$((e - s)) cmd=$*" >> "$d/summary.txt"
exit $rc
