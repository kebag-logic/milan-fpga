#!/usr/bin/env bash
# Launch the #851/#883 processor-copy arms of crflic-mutants (indices 0-5) and
# gsi-mutants' #883 arms (15-18), each its own process, log and rc file.
# usage: launch_arms.sh <repo> <log-dir> <work-dir>
set -u
repo=$1 logs=$2 work=$3
mkdir -p "$logs" "$work"
cd "$repo/tb/verilator/milan_dp"
for i in 0 1 2 3 4 5; do
  ( python3 -B "$(dirname "$0")/run_crflic_pp_arm.py" "$repo" "$i" "$work" > "$logs/crflic_pp$i.log" 2>&1; echo $? > "$logs/crflic_pp$i.rc" ) &
done
for i in 15 16 17 18; do
  ( python3 -B gsi_mutants.py "$i" > "$logs/gsi_$i.log" 2>&1; echo $? > "$logs/gsi_$i.rc" ) &
done
wait
echo done > "$logs/ALL.done"
