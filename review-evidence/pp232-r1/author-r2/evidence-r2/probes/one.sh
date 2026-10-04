#!/usr/bin/env bash
# one reviewer probe, run with the reviewer's script unchanged: one.sh r452|r453 CONTROL
set -u
export PATH=$PINNED_VERILATOR:$PATH
who=$1; c=$2; P=$SCRATCH/r2/probes; s=$(date +%s)
if [ "$who" = r452 ]; then
  bash $SCRATCH/r2/review-evidence/pp232-r1/reviews/R452-1/scripts/clear_cycle_probe.sh $LANE 2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d $P/r452-controls $P/r452-work $c > $P/r452-$c.txt 2>&1
else
  sh $SCRATCH/r2/review-evidence/pp232-r1/reviews/R453-1/scripts/probe_committed.sh $SCRATCH/r2/tree-head $P/r453-controls/$c.sv $P/r453-work/$c aecp_notify pp_top > $P/r453-$c.txt 2>&1
fi
echo "$? $(($(date +%s)-s))" > $P/$who-$c.rc
