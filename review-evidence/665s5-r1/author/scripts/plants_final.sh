#!/bin/bash
# Run named plants one after another in a clone of the head, each its own build directory and log (the final set).
# usage: plants_final.sh CLONE OUT NAME...
set -u
. $MANAGEMENT/2026-09-23/665s5-a702/scripts/env.sh
C=$1 O=$2; shift 2
cd "$C"
for name in "$@"; do
  start=$(date +%s)
  log="$O/logs/plant-$name.log"
  { echo "HEAD $(git -C "$C" rev-parse HEAD)"; echo "\$ python3 -B tb/verilator/ctrl_service_hooks/run.py --plant $name --build-dir <build>/plant-$name"; } > "$log"
  python3 -B tb/verilator/ctrl_service_hooks/run.py --plant "$name" --build-dir "$O/plant-$name" >> "$log" 2>&1
  rc=$?
  echo "elapsed=$(( $(date +%s) - start ))s" >> "$log"
  echo "tree: $(git -C "$C" status --porcelain --untracked-files=all --ignore-submodules=none | wc -l) changed path(s) after the run" >> "$log"
  echo "rc=$rc" >> "$log"
done
