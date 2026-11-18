# cdc.tcl TAG DCP: u_fcdc's storage-to-read-register crossing in one routed checkpoint (RULING-1118e item 3). The
# census of every cdc_pair_fifo and TDM render instance; u_fcdc's storage and read-register cells and their clocks;
# report_cdc -details between those two clocks (filtered to u_fcdc afterwards) and for the whole design;
# report_exceptions and report_timing from the storage to the read register; report_methodology. Read only.
set tag [lindex $argv 0]; set dcp [lindex $argv 1]
set_param general.maxThreads 8
open_checkpoint $dcp
set fh [open fcdc-$tag-cells.txt w]
puts $fh "checkpoint: [file tail [file dirname [file dirname $dcp]]]/[file tail [file dirname $dcp]]/[file tail $dcp]"
foreach inst [lsort [get_cells -hier -quiet -filter {!IS_PRIMITIVE && (ORIG_REF_NAME =~ cdc_pair_fifo* || REF_NAME =~ cdc_pair_fifo* || ORIG_REF_NAME =~ KL_tdm_render* || REF_NAME =~ KL_tdm_render*)}]] {
  puts $fh "census: $inst ([get_property ORIG_REF_NAME $inst] / [get_property REF_NAME $inst])"
}
set all [get_cells -hier -quiet -filter {IS_PRIMITIVE && NAME =~ *u_fcdc*}]
puts $fh "primitives named for u_fcdc: [llength $all]"
set ram [get_cells -hier -quiet -filter {IS_PRIMITIVE && NAME =~ *u_fcdc* && (REF_NAME =~ RAMD* || REF_NAME =~ RAMS* || REF_NAME =~ RAMB*)}]
set rd  [get_cells -hier -quiet -filter {IS_PRIMITIVE && NAME =~ *u_fcdc*rdata_o_reg*}]
set wclk {}; set rclk {}
if {[llength $ram]} {
  puts $fh "storage leaf cells: [llength $ram] ([lsort -unique [get_property REF_NAME $ram]]), e.g. [lindex $ram 0]"
  set wclk [lsort -unique [get_clocks -quiet -of_objects [get_pins -quiet -of_objects $ram -filter {REF_PIN_NAME == CLK || REF_PIN_NAME == CLKARDCLK || REF_PIN_NAME == CLKBWRCLK}]]]
} else { puts $fh "storage leaf cells: 0" }
if {[llength $rd]} {
  puts $fh "read register cells: [llength $rd], e.g. [lindex $rd 0]"
  set rclk [lsort -unique [get_clocks -quiet -of_objects [get_pins -quiet -of_objects $rd -filter {REF_PIN_NAME == C}]]]
} else { puts $fh "read register cells: 0" }
puts $fh "storage write clock(s): $wclk"
puts $fh "read register clock(s): $rclk"
close $fh
report_clock_interaction -delay_type min_max -significant_digits 3 -file fcdc-$tag-clock-interaction.txt
if {[llength $wclk] && [llength $rclk]} {
  report_cdc -details -from [get_clocks $wclk] -to [get_clocks $rclk] -file cdc-clocks-$tag.rpt
  if {[catch {report_exceptions -from $ram -to $rd -file fcdc-$tag-exceptions.txt} e]} {
    set f [open fcdc-$tag-exceptions.txt w]; puts $f "report_exceptions -from storage -to read register: $e"; close $f
  }
  report_timing -from $ram -to $rd -max_paths 4 -nworst 1 -unique_pins -delay_type max -file fcdc-$tag-timing.txt
  report_timing -from $ram -to $rd -max_paths 1 -delay_type min -file fcdc-$tag-timing.txt -append
  report_timing -from [get_clocks $wclk] -to [get_clocks $rclk] -max_paths 1 -file fcdc-$tag-timing-clocks.txt
}
report_cdc -details -file cdc-full-$tag.rpt
report_cdc -summary -file cdc-summary-$tag.rpt
report_methodology -file methodology-full-$tag.rpt
close_design
