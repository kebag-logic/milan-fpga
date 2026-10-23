#!/usr/bin/env bash
# One Vivado session per synthesis (a batch inherits -generic values between synth_design calls).
export PATH=<host path>:$PATH
cd "$(dirname "$0")"
Q=$PWD/KL_render_queue.sv
vivado -mode batch -nojournal -log q1x1.log -source ooc_one.tcl -tclargs $Q KL_render_queue q1x1.rpt N_STREAMS_P=1 N_CH_P=8 FS_HZ_P=48000 MAX_HOLD_NS_P=2126000 EV_LAT_NS_P=20964 N_IF_P=1 IF_LEAD_P=2 PAY_LEAD_CYC_P=16 MAX_EV_P=504 CLK_FREQ_HZ_P=50000000 > q1x1.out 2>&1; echo "q1x1 rc=$?"
vivado -mode batch -nojournal -log q8x8.log -source ooc_one.tcl -tclargs $Q KL_render_queue q8x8.rpt N_STREAMS_P=8 N_CH_P=8 FS_HZ_P=48000 MAX_HOLD_NS_P=2126000 EV_LAT_NS_P=5308 N_IF_P=1 IF_LEAD_P=1 PAY_LEAD_CYC_P=16 MAX_EV_P=504 CLK_FREQ_HZ_P=50000000 > q8x8.out 2>&1; echo "q8x8 rc=$?"
echo OOC-DONE
