#!/bin/sh
# Usage: probe_run.sh <scratch-copy-of-clone> <receipt-dir>
# Runs each probe binary in the leg that grades it, six at a time on CPUs
# 6-11, one log and one rc line per run.
set -u
copy=$1; out=$2
d="$copy/tb/verilator/milan_dp_render"
cd "$d" || exit 99
run() {  # run <name> <mdir> <mode>
  start=$(date +%s)
  taskset -c 6-11 "./$2/Vmilan_dp_tdm8r" "$3" > "$out/probe_$1.log" 2>&1
  echo "$1 $2 $3 rc=$? elapsed=$(( $(date +%s) - start ))" >> "$out/probe_run.rc"
}
: > "$out/probe_run.rc"
run clean_epoch   obj_p_clean   --epoch-only &
run clean_serial  obj_p_clean   --serial-only &
run nodwell_epoch obj_p_nodwell --epoch-only &
run noburst_serial obj_p_noburst --serial-only &
run frozen_serial obj_p_frozen  --serial-only &
run plus2_serial  obj_p_plus2   --serial-only &
wait
run sat3_serial   obj_p_sat3    --serial-only
echo done >> "$out/probe_run.rc"
