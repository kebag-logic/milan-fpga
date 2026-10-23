#!/usr/bin/env bash
# milan_dp_gm_steps: the two stage controls the default run leaves to --all
source $MANAGEMENT/2026-09-23/632-a659/scripts/round4/env.sh
L=$VALIDATION_STORAGE/scratch/632-a659/r4/logs/final
cd $LANES/632-phase/tb/verilator/milan_dp_gm_steps
git rev-parse HEAD > $L/b.head
make -C ../milan_dp gmstep > $L/gmstep.log 2>&1; echo $? > $L/gmstep.rc
python3 $VALIDATION_STORAGE/scratch/632-a659/r4/tools/gm_subset.py "the refused PDUs are not counted" "a gap in the presented frames leaves no counted slip" > $L/gmstep_subset.log 2>&1; echo $? > $L/gmstep_subset.rc
echo DONE > $L/b.done
