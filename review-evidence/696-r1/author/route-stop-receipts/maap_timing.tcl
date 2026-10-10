set_param general.maxThreads 8
open_checkpoint {$VALIDATION_STORAGE/696-a570/resume-differential/shipping/ax7101/gateware/alinx_ax7101_route.dcp}
set maap [get_cells -hierarchical -filter {IS_SEQUENTIAL && NAME =~ "*g_maap.maap_engine/*"}]
puts "MAAP sequential cells: [llength $maap]"
report_timing -to $maap -max_paths 3 -nworst 1 -delay_type max -file maap_to.rpt
report_timing -from $maap -max_paths 3 -nworst 1 -delay_type max -file maap_from.rpt
report_timing -max_paths 10 -nworst 1 -delay_type max -file worst10.rpt
foreach dir {to from} {
  if {$dir eq "to"} {set p [get_timing_paths -to $maap -max_paths 1 -delay_type max]} else {set p [get_timing_paths -from $maap -max_paths 1 -delay_type max]}
  puts "MAAP $dir worst slack: [get_property SLACK $p] ns, levels [get_property LOGIC_LEVELS $p], [get_property STARTPOINT_PIN $p] -> [get_property ENDPOINT_PIN $p]"
}
set w [get_timing_paths -max_paths 1 -delay_type max]
puts "design worst slack: [get_property SLACK $w] ns, [get_property STARTPOINT_PIN $w] -> [get_property ENDPOINT_PIN $w]"
quit
