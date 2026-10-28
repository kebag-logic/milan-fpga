#!/bin/bash
# The acknowledgement plants: each applied to the scratch worktree in turn, a real 1x1 build, then reverted.
set -u
O=$MANAGEMENT/2026-09-23/665s1-a680j/probes
W=$VALIDATION_STORAGE/scratch/665s1-a680j-work/plant
for p in ack-early ack-probe; do
  git -C "$W" apply "$O/plant-$p.diff"
  "$O/leg.sh" "$W" "plant-$p-1x1" 1x1 --groups aecp --jobs 4
  git -C "$W" checkout -q tb/verilator/ctrl_service_budget/split_soc.py
done
