set SPEC [file normalize [file dirname [info script]]/../..]
read_verilog -sv $SPEC/hdl/aecp/ucpu_pkg.sv $SPEC/hdl/aecp/KL_aecp_ucpu.sv
synth_design -mode out_of_context -top KL_aecp_ucpu -part xc7a100tfgg484-2
create_clock -period 10.000 -name clk [get_ports clk_i]
report_utilization -hierarchical -file util_hier.rpt
report_utilization -file util.rpt
report_timing_summary -delay_type max -max_paths 3 -file timing.rpt
