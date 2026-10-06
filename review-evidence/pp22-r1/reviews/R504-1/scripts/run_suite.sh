#!/usr/bin/env bash
# Run one processor suite (its Makefile default goal) in an exported tree with
# the job-capped pinned Verilator. usage: run_suite.sh <tree> <suite> <log> <rcfile> [vjobs]
set -u
tree=$1; suite=$2; log=$3; rcf=$4; export VJOBS=${5:-4}
here=$(dirname "$(readlink -f "$0")")
rc=0
( cd "$tree/tb/$suite" && /usr/bin/time -f 'maxrss_kb=%M wall_s=%e' \
    make VERILATOR="$here/verilator_jcap.sh" ) > "$log" 2>&1 || rc=$?
echo "$rc" > "$rcf"
