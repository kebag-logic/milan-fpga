#!/usr/bin/env bash
# usage: focused_suites.sh <head tree> <out dir> -- runs the changed/merged suites one by one
set -u
H=$1; O=$2; P=$(cd "$(dirname "$0")/.." && pwd)   # the packet root
for s in "srp_stream_fsms make" "acmp_listener make run" "srp_top make run" "srp_encoder make" "srp_decoder make" "event_router make"; do
  set -- $s; d=$1; shift
  $P/scripts/run_job.sh "$O" "suite-$d" "$H/tb/$d" "$@" VERILATOR=$P/scratch/bin/verilator
done
echo done > "$O/focused.done"
