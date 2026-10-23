#!/usr/bin/env bash
export PATH=<host path>:$PATH
cd "$(dirname "$0")"
G="N_STREAMS_P=1 N_CH_P=8 FS_HZ_P=48000 MAX_HOLD_NS_P=2126000 EV_LAT_NS_P=20964 N_IF_P=1 IF_LEAD_P=2 PAY_LEAD_CYC_P=16 CLK_FREQ_HZ_P=50000000"
vivado -mode batch -nojournal -log old.log -source ooc_clk.tcl -tclargs $PWD/old.sv KL_render_queue old.rpt $G > old.out 2>&1; echo "old rc=$?"
vivado -mode batch -nojournal -log new.log -source ooc_clk.tcl -tclargs $PWD/new.sv KL_render_queue new.rpt $G MAX_EV_P=504 > new.out 2>&1; echo "new rc=$?"
echo DONE
