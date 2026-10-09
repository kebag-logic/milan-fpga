#!/bin/bash
# Usage: run_suite.sh <tree> <logprefix> <cpus> [extra make args...]
# Replicates the sweep's invocation: timeout 1800 make -C <dir>, MAKEFLAGS unset.
tree=$1; pre=$2; cpus=$3; shift 3
start=$(date +%s.%N)
env -u MAKEFLAGS -u MFLAGS taskset -c "$cpus" timeout 1800 make -C "$tree/tb/verilator/follow_ring" "$@" > "$pre.log" 2>&1
rc=$?
end=$(date +%s.%N)
echo "rc=$rc wall_s=$(echo "$end - $start" | bc)" > "$pre.rc"
