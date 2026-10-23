#!/usr/bin/env bash
# One Vivado session per synthesis (a batch inherits -generic values between synth_design calls).
# KL_mtt_round at N_P = 2 (round 4's 1x1 binding: the AAF talker and the CRF output), 9 (the 8x8 binding: eight
# AAF talkers and the CRF output) and 1 (this round's binding: the CRF output alone).
export PATH=<vivado>
cd "$(dirname "$0")"
M=<repo>/hdl/ieee1722/crf/KL_mtt_round.sv
for n in 1 2 9; do
  vivado -mode batch -nojournal -log m$n.log -source ooc_one.tcl -tclargs $M KL_mtt_round m$n.rpt N_P=$n BASE_HZ_P=48000 > m$n.out 2>&1; echo "m$n rc=$?"
done
echo OOC-DONE
