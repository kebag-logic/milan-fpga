# The unchanged complete-processor OOC recipe, then the #181 cone reports.
# vivado -mode batch -source ooc_cone.tcl -tclargs <tree> <n_in> <n_out>
set TREE [file normalize [lindex $argv 0]]
source $TREE/syn/ooc/protocol_processor_ooc.tcl
set src [get_cells -hier -filter {NAME =~ *u_notify/cmdq_count_r_reg*}]
set dst [get_cells -hier -filter {NAME =~ *u_event_router/sel_r_reg*}]
puts "CONE src [llength $src] dst [llength $dst]"
report_timing -from $src -to $dst -max_paths 10 -nworst 1 -file cone.rpt
report_timing -from $src -to $dst -max_paths 1 -nworst 1 -sort_by group -file cone_worst.rpt
report_design_analysis -logic_level_distribution -of_timing_paths [get_timing_paths -from $src -to $dst -max_paths 1000 -nworst 1] -file cone_levels.rpt
report_design_analysis -logic_level_distribution -file levels_all.rpt
report_timing -max_paths 20 -nworst 1 -file top20.rpt
# where else the notify occupancy and the router select now end and begin
report_timing -from $src -max_paths 5 -nworst 1 -file from_cmdq.rpt
report_timing -to $dst -max_paths 5 -nworst 1 -file to_sel.rpt
set mid [get_cells -hier -filter {NAME =~ *u_notify/cmdq_nempty_r_reg*}]
puts "CUT mid [llength $mid]"
if {[llength $mid] > 0} {
  report_timing -from $src -to $mid -max_paths 1 -nworst 1 -file count_to_nempty.rpt
  report_timing -from $mid -to $dst -max_paths 3 -nworst 1 -file nempty_to_sel.rpt
  report_timing -from $mid -max_paths 3 -nworst 1 -file from_nempty.rpt
}
