set_param general.maxThreads 4
read_verilog -sv [list src/KL_mbx_pkg.sv src/KL_mbx_dma.sv]
synth_design -mode out_of_context -top KL_mbx_dma -part xc7a100tfgg484-2
report_utilization -file synth_util.rpt
create_clock -period 10.000 -name clk [get_ports clk_i]
opt_design
place_design
route_design
report_utilization -file route_util.rpt
report_timing_summary -delay_type min_max -file timing.rpt
report_route_status -file route.rpt
puts "PRICED KL_mbx_dma"
