#!/usr/bin/env bash
# media_phase: the whole planted-defect campaign at the lane head, one build at a time
source $MANAGEMENT/2026-09-23/632-a659/scripts/round4/env.sh
L=$VALIDATION_STORAGE/scratch/632-a659/r4/logs/final
cd $LANES/632-phase/tb/verilator/media_phase
git rev-parse HEAD > $L/e.head
date -Is > $L/mp_mutants.start
make mutants MUTANT_JOBS=1 > $L/mp_mutants.log 2>&1; echo $? > $L/mp_mutants.rc
date -Is > $L/mp_mutants.end
echo DONE > $L/e.done
