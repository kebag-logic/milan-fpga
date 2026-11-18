#!/bin/bash
# Run a chain of make targets in a tb/verilator directory; stop at the first failure.
# usage: dp_chain.sh <tbdir> <target...>; VERILATOR and VERILATOR_JOBS from the environment
d=$1; shift
for t in "$@"; do
  echo "== make -C $d $t $(date +%T)"
  make -C "$d" VERILATOR="$VERILATOR" VERILATOR_JOBS="$VERILATOR_JOBS" "$t" || { echo "FAILED $d $t"; exit 1; }
done
echo "CHAIN PASS $d"
