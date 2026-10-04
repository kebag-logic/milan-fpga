# Standalone OOC synthesis of KL_crf_rx at milan_datapath's binding (#653 area).
set SRC $::env(CRF_SRC)
set TAG $::env(TAG)
read_verilog -sv $SRC
synth_design -top KL_crf_rx -part xc7a100tfgg484-2 -mode out_of_context \
  -generic CLK_FREQ_HZ_P=100000000 -generic IVAL_CYC_P=100000000
report_utilization -file util_$TAG.rpt
