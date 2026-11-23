set_param general.maxThreads 8
read_verilog -sv $CHECKOUT/hdl/ieee1722/aaf/KL_chan_map_capture.sv
read_verilog -sv $SCRATCH/leaf-capture/capture_leaf.sv
synth_design -mode out_of_context -top capture_leaf -part xc7a100t-fgg484-2 -directive AreaOptimized_high -generic INPUT_LOOPBACK_P=1 -generic LEGACY_P=0 -generic N_LB_STREAMS_P=1 -generic N_LB_CH_P=2
create_clock -period 20 [get_ports clk_i]
opt_design -directive ExploreArea
report_utilization -hierarchical -file leaf_hier.rpt
report_utilization -file leaf_util.rpt
write_checkpoint -force leaf.dcp
quit
