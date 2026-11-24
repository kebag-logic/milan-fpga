#!/bin/bash
# tsrun.sh OUTDIR CMD...: run CMD under perf stat (counting children), every output line prefixed with seconds since start
set -u
O=$1; shift
mkdir -p "$O"
. /data-2/milan/tmp/cicd-a839/bin/env.sh
start=$(date +%s.%N)
echo "$*" > "$O/cmd"
( /usr/bin/time -v -o "$O/time.txt" perf stat -o "$O/perf.txt" -e task-clock,instructions:u,cycles:u -- "$@" 2>&1; echo "RC=$?" ) |
  while IFS= read -r line; do printf '%8.1f %s\n' "$(echo "$(date +%s.%N) - $start" | bc)" "$line"; done > "$O/out.log"
tail -3 "$O/out.log"
