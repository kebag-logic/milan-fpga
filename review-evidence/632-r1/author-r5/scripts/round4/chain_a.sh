#!/usr/bin/env bash
# milan_dp: the true-ratio leg, its render mutants and the CSR controls, at the lane head
source $MANAGEMENT/2026-09-23/632-a659/scripts/round4/env.sh
L=$VALIDATION_STORAGE/scratch/632-a659/r4/logs/final
cd $LANES/632-phase/tb/verilator/milan_dp
git rev-parse HEAD > $L/a.head
make -j8 aclk > $L/aclk.log 2>&1; echo $? > $L/aclk.rc
python3 render_mutants.py > $L/dp_render_mutants.log 2>&1; echo $? > $L/dp_render_mutants.rc
make render-csr-controls > $L/dp_csr_controls.log 2>&1; echo $? > $L/dp_csr_controls.rc
echo DONE > $L/a.done
