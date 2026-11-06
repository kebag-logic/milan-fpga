#!/bin/sh
# Usage: run_suites.sh <scratch-root> <receipts-dir> <verilator>
# Runs tb/pp_top and tb/srp_stream_fsms "make run" in disposable clones
# pp-6162885 (round-4 head) and pp-834cc88 (round-3 head) concurrently,
# one log and rc file per job.
S=$1; R=$2; V=$3
for c in 6162885 834cc88; do
  for t in pp_top srp_stream_fsms; do
    ( cd "$S/pp-$c/tb/$t" && make run VERILATOR="$V" > "$R/$t-$c.log" 2>&1; echo $? > "$R/$t-$c.rc" ) &
  done
done
wait
