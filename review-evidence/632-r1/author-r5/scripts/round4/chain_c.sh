#!/usr/bin/env bash
# follow_ring: the six planted controls (builds capped at -j8 and two Verilator jobs)
source $MANAGEMENT/2026-09-23/632-a659/scripts/round4/env.sh
L=$VALIDATION_STORAGE/scratch/632-a659/r4/logs/final
cd $LANES/632-phase/tb/verilator/follow_ring
git rev-parse HEAD > $L/c.head
python3 $VALIDATION_STORAGE/scratch/632-a659/r4/tools/fr_subset.py --jobs 1 > $L/fr_mutants.log 2>&1; echo $? > $L/fr_mutants.rc
echo DONE > $L/c.done
