#!/bin/bash
# Run reviewer probes (round-1 sets and the per-octet set) against the head campaign's baseline.
# Usage: run_probes.sh TREE OUT_DIR JOBS
set -u
source "$(dirname "$0")/env.sh"
T=$1; O=$2; J=$3; W=$P/scratch/work; B=$W/mut/baseline
for set in probes probes2 octet-probes; do
  src=$O/$set.json; [ -f "$src" ] || src=$P/scratch/$set.json
  cp "$src" "$O/$set.json" 2>/dev/null
  python3 "$(dirname "$0")/probes_run.py" $T $B "$O/$set.json" $W/probes-$set "$O/$set-results.json" $J >"$O/$set-run.log" 2>&1
  echo $? >"$O/$set.rc"
done
echo done >"$O/PROBES.done"
