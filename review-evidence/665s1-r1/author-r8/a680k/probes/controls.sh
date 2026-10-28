#!/bin/bash
# The as-built control at 1x1 from the lane checkout, then its planted control in the scratch worktree:
# the same run with the CPU generator handed the regions' cover (a CPU that decodes correctly, so the
# image boots clean), which must escape.
set -u
O=$MANAGEMENT/2026-09-23/665s1-a680k/probes
C=$LANES/665-s1-faces
W=$VALIDATION_STORAGE/scratch/665s1-a680j-work/plant
"$O/leg.sh" "$C" C-asbuilt 1x1 --cpu-regions as-built --jobs 4
git -C "$W" apply "$O/plant-asbuilt-clean.diff"
"$O/leg.sh" "$W" plant-asbuilt-clean-1x1 1x1 --cpu-regions as-built --jobs 4
git -C "$W" checkout -q tb/verilator/ctrl_service_budget/split_soc.py
