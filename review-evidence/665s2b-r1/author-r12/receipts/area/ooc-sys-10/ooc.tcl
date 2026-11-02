set_param general.maxThreads 8
read_verilog [list Ram_1w_1rs_Generic.v Ram_1w_1ra_Generic.v VexiiRiscvLitex_7ee512a1cb1c336731b7f28188c9814f.v sim.v]
synth_design -mode out_of_context -directive AreaOptimized_high -part xc7a100t-fgg484-2 -top sim
report_utilization -file synth_util.rpt
create_clock -period 10 -name sys_clk [get_ports sys_clk]
opt_design
place_design
route_design
report_utilization -file route_util.rpt
report_utilization -hierarchical -hierarchical_depth 4 -hierarchical_min_primitive_count 0 -file route_hier.rpt
report_timing_summary -delay_type min_max -file timing.rpt
report_timing -delay_type max -max_paths 10 -group sys_clk -file paths_sys.rpt
report_clock_interaction -file clock_interaction.rpt
report_route_status -file route.rpt
puts "ROUTED sys_clk 10 ns"
