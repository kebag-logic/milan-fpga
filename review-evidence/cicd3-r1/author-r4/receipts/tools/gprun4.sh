#!/bin/bash
# gprun4.sh TREE CPUS TAG JOBS: FPGA-gPTP `make -jJOBS -C tb/verilator/engine run` from r4/gp/TREE pinned to CPUS, core
# dumps off; time, counters, transcript (stdout and stderr merged, as round 3), rc. Output: r4/gpout/TAG/
set -u
T=$1; C=$2; G=$3; J=$4; O=/data-2/milan/tmp/cicd-a839/r4/gpout/$G
. /data-2/milan/tmp/cicd-a839/r4/bin/env.sh
export MAKEFLAGS="-j$J --no-print-directory" VERILATOR_JOBS=4
ulimit -c 0
rm -rf "$O"; mkdir -p "$O"; cd /data-2/milan/tmp/cicd-a839/r4/gp/$T/tb/verilator/engine || exit 99
git rev-parse HEAD > "$O/head"; make -s clean >/dev/null 2>&1
date +%s.%N > "$O/start"
taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/time" \
  perf stat -x, -o "$O/perf" -e task-clock,cycles:u,instructions:u -- make run > "$O/log" 2>&1
echo "rc=$?" >> "$O/time"; date +%s.%N > "$O/end"; echo "$G $(head -1 "$O/time") $(tail -1 "$O/time")"
