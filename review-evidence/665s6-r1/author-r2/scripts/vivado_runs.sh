#!/bin/bash
# Under the host Vivado lock (the caller holds it): the one split-image placement at the head (the xvlog gate ran earlier).
# Start ONLY as: setsid nohup flock $VIVADO_LOCK bash vivado_runs.sh > <log> 2>&1 &   (never beside a sweep)
G=$HOME/milan-fpga-management/2026-09-23/665s6-a745b/scripts/gate.sh
F=$VALIDATION_STORAGE/scratch/665s6-a745b/final
W=$VALIDATION_STORAGE/scratch/665s6-a745b/place
mkdir -p $W
echo "lock held from $(date -u +%FT%TZ); MemAvailable $(awk '/MemAvailable/ {print int($2/1048576)}' /proc/meminfo) GB"
$G split-place $VALIDATION_STORAGE/scratch/665s6-a745b/fwclone bash $HOME/milan-fpga-management/2026-09-23/665s6-a745b/scripts/split_place.sh $VALIDATION_STORAGE/scratch/665s6-a745b/fwclone $VALIDATION_STORAGE/scratch/665s6-a745b/splitfw/plat/ctrl_app.elf $W
echo "lock released at $(date -u +%FT%TZ)"
