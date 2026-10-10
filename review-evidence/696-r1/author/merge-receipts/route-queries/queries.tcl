set_param general.maxThreads 8
open_checkpoint {<scratch>/shipping/ax7101/gateware/alinx_ax7101_route.dcp}
set maap [get_cells -hierarchical -filter {IS_SEQUENTIAL && NAME =~ "*g_maap.maap_engine/*"}]
puts "MAAP sequential cells: [llength $maap]"
report_timing -to $maap -max_paths 3 -nworst 1 -delay_type max -file maap_to.rpt
report_timing -from $maap -max_paths 3 -nworst 1 -delay_type max -file maap_from.rpt
report_timing -to $maap -max_paths 3 -nworst 1 -delay_type min -file maap_to_hold.rpt
report_timing -max_paths 10 -nworst 1 -delay_type max -file worst10.rpt
report_timing -max_paths 1 -nworst 1 -delay_type max -file worst_path.rpt
foreach dir {to from} {
  if {$dir eq "to"} {set p [get_timing_paths -to $maap -max_paths 1 -delay_type max]} else {set p [get_timing_paths -from $maap -max_paths 1 -delay_type max]}
  puts "MAAP $dir worst setup slack: [get_property SLACK $p] ns, levels [get_property LOGIC_LEVELS $p], [get_property STARTPOINT_PIN $p] -> [get_property ENDPOINT_PIN $p]"
}
set h [get_timing_paths -to $maap -max_paths 1 -delay_type min]
puts "MAAP to worst hold slack: [get_property SLACK $h] ns"
set x [get_timing_paths -max_paths 1 -delay_type max]
puts "design worst setup slack: [get_property SLACK $x] ns, levels [get_property LOGIC_LEVELS $x], [get_property STARTPOINT_PIN $x] -> [get_property ENDPOINT_PIN $x]"
quit
