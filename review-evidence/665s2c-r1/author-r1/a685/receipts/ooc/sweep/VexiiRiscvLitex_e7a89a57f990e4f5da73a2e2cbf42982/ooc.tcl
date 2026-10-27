set_param general.maxThreads 8
read_verilog [list Ram_1w_1rs_Generic.v Ram_1w_1ra_Generic.v VexiiRiscvLitex_e7a89a57f990e4f5da73a2e2cbf42982.v]
synth_design -mode out_of_context -directive AreaOptimized_high -part xc7a100t-fgg484-2 -top VexiiRiscvLitex_e7a89a57f990e4f5da73a2e2cbf42982
report_utilization -file synth_util.rpt
report_utilization -hierarchical -hierarchical_depth 4 -hierarchical_min_primitive_count 0 -file synth_hier.rpt
create_clock -period 20.000 -name cpu_clk [get_ports cpu_clk]
create_clock -period 10.000 -name litex_clk [get_ports litex_clk]
set_clock_groups -asynchronous -group cpu_clk -group litex_clk
opt_design
place_design
route_design
report_utilization -file route_util.rpt
report_utilization -hierarchical -hierarchical_depth 4 -hierarchical_min_primitive_count 0 -file route_hier.rpt
report_timing_summary -delay_type min_max -file timing.rpt
report_route_status -file route.rpt
puts "PRICED VexiiRiscvLitex_e7a89a57f990e4f5da73a2e2cbf42982"
