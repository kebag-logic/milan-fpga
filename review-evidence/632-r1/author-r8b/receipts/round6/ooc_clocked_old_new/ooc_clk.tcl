# usage: vivado -mode batch -source ooc_clk.tcl -tclargs <file> <top> <report> <generic>...
set f [lindex $argv 0]
set top [lindex $argv 1]
set rpt [lindex $argv 2]
set gen {}
foreach g [lrange $argv 3 end] { lappend gen -generic $g }
read_verilog -sv $f
read_xdc -mode out_of_context clk.xdc
synth_design -mode out_of_context -top $top -part xc7a100tfgg484-2 -directive AreaOptimized_high {*}$gen
report_utilization -file $rpt
report_utilization -hierarchical -file ${rpt}.hier
