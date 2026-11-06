#!/bin/sh
# S3's split boot at both shapes, then R737-4's partial_map_probe.sh unedited and this round's map_edges.sh on the
# real generated map, on one clean clone; each step in sequence, because a boot's export writes the checkout's ignored
# outputs. None of the round's named gates links a real map, so these show a complete one is still accepted.
J="$MANAGEMENT/2026-09-23/665s4-a698i/scripts/job.sh"; C=$VALIDATION_STORAGE/scratch/665s4-a698i/wt-boot; S=$VALIDATION_STORAGE/scratch/665s4-a698i; R=$REVIEWS
RUN="python3 -B tb/verilator/ctrl_split_boot/run.py"
$J boot-1x1 $C $RUN --build-dir $S/boot-1x1
$J boot-8x8 $C $RUN --build-dir $S/boot-8x8 --shape endstation_ax7101_8x8
$J partial-map-probe $C bash $R/665s4-r737-4-packet/scripts/partial_map_probe.sh $C $S/boot-1x1 $S/partial-map-probe-out
$J map-edges $C bash $MANAGEMENT/2026-09-23/665s4-a698i/scripts/map_edges.sh $C $S/boot-1x1 $S/map-edges-out
$J py-idiom $C python3 scripts/check_py_idiom.py
git -C $C status --porcelain --untracked-files=all --ignore-submodules=none > $S/wt-boot.status-after
echo done > $S/seq-boots.done
