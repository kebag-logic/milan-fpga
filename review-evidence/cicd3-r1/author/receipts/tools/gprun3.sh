#!/bin/bash
# gprun3.sh TREE CPUS TAG: FPGA-gPTP `make -C tb/verilator/engine run` from r3/TREE pinned to CPUS; time and counters.
set -u
T=$1; C=$2; G=$3; O=/data-2/milan/tmp/cicd-a839/r3/gp/$G
. /data-2/milan/tmp/cicd-a839/r3/bin/env.sh
export MAKEFLAGS='-j1 --no-print-directory' VERILATOR_JOBS=4
rm -rf "$O"; mkdir -p "$O"; cd /data-2/milan/tmp/cicd-a839/r3/$T/tb/verilator/engine || exit 99
make -s clean >/dev/null 2>&1
taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/time" \
  perf stat -x, -o "$O/perf" -e task-clock,cycles:u,instructions:u -- make run > "$O/log" 2>&1
echo "rc=$?" >> "$O/time"; echo "$G $(head -1 "$O/time") $(tail -1 "$O/time")"
