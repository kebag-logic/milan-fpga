#!/bin/bash
# ab.sh OUTPREFIX DIR CMD...: run CMD in DIR under perf stat + /usr/bin/time; stdout+stderr to OUTPREFIX.log
set -u
O=$1; D=$2; shift 2
. /data-2/milan/tmp/cicd-a839/bin/env.sh
mkdir -p "$(dirname "$O")"
cd "$D" || exit 99
echo "$*" > "$O.cmd"
/usr/bin/time -f "%e wall %U user %S sys %M maxrssKB" -o "$O.time" perf stat -x, -o "$O.perf" -e task-clock,cycles:u,instructions:u -- "$@" > "$O.log" 2>&1
echo "RC=$?" >> "$O.time"
