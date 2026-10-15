# usage: vivado -mode batch -source ooc.tcl -tclargs <name>
set name [lindex $argv 0]
read_verilog -sv $name.sv
synth_design -top settle_ooc -part xc7a100tfgg484-2 -mode out_of_context -flatten_hierarchy full
create_clock -period 20.000 -name axis_clk [get_ports axis_clk]
report_utilization -file $name.vivado.util.txt
report_timing_summary -file $name.vivado.timing.txt
