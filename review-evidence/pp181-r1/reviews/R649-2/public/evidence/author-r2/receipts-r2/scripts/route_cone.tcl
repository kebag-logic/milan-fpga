# Report the #181 cone on a routed checkpoint (read only; reports go to the cwd).
# vivado -mode batch -source route_cone.tcl -tclargs <route.dcp>
open_checkpoint [lindex $argv 0]
set pp milan_datapath/pp_shadow/u_pp
set src [get_cells -hier -filter "NAME =~ $pp/u_notify/cmdq_count_r_reg*"]
set dst [get_cells -hier -filter "NAME =~ $pp/u_event_router/sel_r_reg*"]
puts "CONE src [llength $src] dst [llength $dst]"
report_timing -from $src -to $dst -max_paths 3 -nworst 1 -file cone.rpt
report_timing -to $dst -max_paths 5 -nworst 1 -file to_sel.rpt
report_timing -from $src -max_paths 5 -nworst 1 -file from_cmdq.rpt
set rtr [get_cells -hier -filter "NAME =~ $pp/u_event_router/* && IS_SEQUENTIAL"]
report_timing -to $rtr -max_paths 5 -nworst 1 -file to_router.rpt
report_timing -group milansoc_crg_clkout1 -max_paths 10 -nworst 1 -file clkout1_top10.rpt
# the two halves of the cut cone at head: count -> registered occupancy, occupancy -> select
set mid [get_cells -hier -filter "NAME =~ $pp/u_notify/cmdq_nempty_r_reg*"]
puts "CUT mid [llength $mid]"
if {[llength $mid] > 0} {
  report_timing -from $src -to $mid -max_paths 1 -nworst 1 -file count_to_nempty.rpt
  report_timing -from $mid -to $dst -max_paths 3 -nworst 1 -file nempty_to_sel.rpt
  report_timing -from $mid -max_paths 3 -nworst 1 -file from_nempty.rpt
}
