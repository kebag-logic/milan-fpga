set_param general.maxThreads 8
read_verilog -sv $CHECKOUT/hdl/ieee1722/aaf/KL_render_queue.sv
synth_design -mode out_of_context -top KL_render_queue -part xc7a100t-fgg484-2 -directive AreaOptimized_high -generic INPUT_LOOPBACK_P=1 -generic CLK_FREQ_HZ_P=50000000 -generic IF_LEAD_P=1
create_clock -period 20 [get_ports clk_i]
opt_design -directive ExploreArea
report_utilization -hierarchical -file leaf_hier.rpt
report_utilization -file leaf_util.rpt
write_checkpoint -force leaf.dcp
quit
