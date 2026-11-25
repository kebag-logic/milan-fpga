#!/bin/bash
# execs.sh TREE CPUS TAG CASE...: in r7/wt/TREE, run each CASE's `make exec-CASE` (the command the CI driver runs)
# one after another, pinned to CPUS; stdout+stderr in r7/meas/TREE/TAG-CASE.out, the [#207] line in progress.
set -u
T=$1; C=$2; G=$3; shift 3; R=/data-2/milan/tmp/cicd-a839/r7; O=$R/meas/$T
. $R/bin/env.sh
export MAKEFLAGS='--no-print-directory'
mkdir -p "$O"; cd "$R/wt/$T" || exit 99
for k in "$@"; do
  taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/$G-$k.time" \
    make -s --no-print-directory -C tb/verilator/milan_dp "exec-$k" > "$O/$G-$k.out" 2>&1
  echo "rc=$?" >> "$O/$G-$k.time"
  echo "$T $G $k cpus=$C: $(head -1 "$O/$G-$k.time") $(tail -1 "$O/$G-$k.time") | $(grep -m1 '^\[#207\]' "$O/$G-$k.out") | $(grep -m1 -E '^[0-9]+ checks' "$O/$G-$k.out")" >> $R/meas/progress
done
