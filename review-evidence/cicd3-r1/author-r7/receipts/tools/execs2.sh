#!/bin/bash
# execs2.sh TREE CPUS TAG CASE...: as execs.sh, with stdout and stderr kept apart, as ci_make_cases.py keeps them,
# so sha256(stdout + stderr) is the receipt's output_sha256 for the case. Output in r7/meas/TREE/TAG-CASE.{stdout,stderr}.
set -u
T=$1; C=$2; G=$3; shift 3; R=/data-2/milan/tmp/cicd-a839/r7; O=$R/meas/$T
. $R/bin/env.sh
export MAKEFLAGS='--no-print-directory'
mkdir -p "$O"; cd "$R/wt/$T" || exit 99
for k in "$@"; do
  taskset -c "$C" /usr/bin/time -f "%e wall %U user %S sys" -o "$O/$G-$k.time" \
    make -s --no-print-directory -C tb/verilator/milan_dp "exec-$k" > "$O/$G-$k.stdout" 2> "$O/$G-$k.stderr"
  echo "rc=$?" >> "$O/$G-$k.time"
  sha=$(cat "$O/$G-$k.stdout" "$O/$G-$k.stderr" | sha256sum | cut -c1-16)
  echo "$T $G $k cpus=$C: $(head -1 "$O/$G-$k.time") $(tail -1 "$O/$G-$k.time") | out $sha | $(grep -m1 '^\[#207\]' "$O/$G-$k.stdout") | $(grep -m1 -E '^[0-9]+ checks' "$O/$G-$k.stdout")" >> $R/meas/progress
done
