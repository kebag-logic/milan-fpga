#!/bin/bash
# Run named plants one after another in a checkout, each its own log; "name:reuse" reuses that plant's build.
# usage: plants_chain.sh CHECKOUT TMP NAME[:reuse]...
set -u
. $MANAGEMENT/2026-09-23/665s5-a702/scripts/env.sh
C=$1 T=$2; shift 2
cd "$C"
for item in "$@"; do
  name=${item%%:*}; extra=""; [ "$item" != "$name" ] && extra="--reuse-build"
  start=$(date +%s)
  { echo "HEAD $(git -C "$C" rev-parse HEAD)"; echo "\$ python3 -B tb/verilator/ctrl_service_hooks/run.py --plant $name $extra --build-dir <tmp>/p-$name"; } > "$T/logs/p-$name.log"
  python3 -B tb/verilator/ctrl_service_hooks/run.py --plant "$name" $extra --build-dir "$T/p-$name" >> "$T/logs/p-$name.log" 2>&1
  rc=$?
  echo "elapsed=$(( $(date +%s) - start ))s" >> "$T/logs/p-$name.log"
  echo "rc=$rc" >> "$T/logs/p-$name.log"
done
