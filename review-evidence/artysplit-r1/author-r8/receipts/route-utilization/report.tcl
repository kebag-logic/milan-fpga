# Post-route utilization of a retained routed checkpoint; no implementation step.
set dcp [lindex $argv 0]
set out [lindex $argv 1]
open_checkpoint $dcp
report_utilization -file $out
report_utilization -hierarchical -hierarchical_depth 1 -file ${out}.hier
puts "DESIGN_STATE [get_property DESIGN_STATE [current_design]]"
