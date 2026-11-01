#!/bin/bash
# Repeat the untouched lifecycle test: lifecycle_repeat.sh <tree> <label> <count> <outdir>
cd "$1" || exit 2
for i in $(seq 1 "$3"); do
  start=$(date +%s); python3 tb/verilator/gptp_shadow/test_mutant_lifecycle.py > "$4/$2-$i.log" 2>&1; rc=$?
  echo "$2 $i rc=$rc wall=$(( $(date +%s)-start ))s load=$(cut -d' ' -f1 /proc/loadavg) $(grep -m1 -o 'CLEANUP FAILED[^{]*' "$4/$2-$i.log")" >> "$4/summary.txt"
done
