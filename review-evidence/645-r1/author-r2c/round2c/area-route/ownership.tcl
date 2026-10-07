if {[llength $argv] != 2} { error "Usage: ownership.tcl <head-route.dcp> <base-route.dcp>" }
set_param general.maxThreads 1
open_checkpoint [lindex $argv 0]
report_route_status -file candidate_route_status.rpt
# Full timing comes from the implementation corner reports.
# Attribute the new settle state and a conservative complete LUT cone.
set added [get_cells -hier -filter {IS_PRIMITIVE && PRIMITIVE_GROUP == FLOP_LATCH && (NAME =~ *settle_run_ticks_r_reg* || NAME =~ *settle_ceil_ticks_r_reg* || NAME =~ *settle_pend_r_reg* || NAME =~ *settle_recover_r_reg* || NAME =~ *settle_recentre_p_r_reg*)}]
set f [open candidate_settle_cells.tsv w]
foreach c $added { puts $f "$c\t[get_property REF_NAME $c]" }
close $f
if {[llength $added] < 1} { error "No new settle registers for ownership attribution" }
set inputs [get_pins -of_objects $added -filter {DIRECTION == IN && REF_PIN_NAME != C}]
set cones [all_fanin -flat -only_cells -to $inputs]
set pulse [get_cells -hier -filter {IS_PRIMITIVE && PRIMITIVE_GROUP == FLOP_LATCH && NAME =~ *settle_recentre_p_r_reg*}]
if {[llength $pulse] < 1} { error "No settle pulse register" }
set qo [get_pins -of_objects $pulse -filter {DIRECTION == OUT}]
set cones [concat $cones [all_fanout -flat -only_cells -from $qo]]
set head_lut_names [dict create]
set f [open candidate_settle_cone.tsv w]
foreach c [lsort -unique $cones] {
  set kind [get_property REF_NAME $c]
  if {[string match LUT* $kind]} {
    dict set head_lut_names [get_property NAME $c] 1
    set terms {}
    foreach ip [lsort [get_pins -of_objects $c -filter {DIRECTION == IN}]] {
      set nets [get_nets -of_objects $ip]
      set drivers [lsort [concat [get_pins -leaf -of_objects $nets -filter {DIRECTION == OUT}] [get_ports -of_objects $nets -filter {DIRECTION == IN}]]]
      lappend terms "[get_property REF_PIN_NAME $ip]=[join $drivers ,]"
    }
    puts $f "$c\t$kind\t[get_property INIT $c]\t[join $terms ;]"
  }
}
close $f
set cap [get_cells -hier -filter {ORIG_REF_NAME == KL_chan_map_capture || REF_NAME == KL_chan_map_capture}]
if {[llength $cap] != 1} { error "Expected one capture crossbar" }
report_utilization -cells $cap -file candidate_capture_utilization.rpt

# Compare with the historical routed base without releasing the shared lock.
close_design
open_checkpoint [lindex $argv 1]
set f [open base_lut_logic.tsv w]
foreach c [lsort [get_cells -hier -filter {IS_PRIMITIVE && REF_NAME =~ LUT*}]] {
  if {![dict exists $head_lut_names [get_property NAME $c]]} { continue }
  set kind [get_property REF_NAME $c]
  set terms {}
  foreach ip [lsort [get_pins -of_objects $c -filter {DIRECTION == IN}]] {
    set nets [get_nets -of_objects $ip]
    set drivers [lsort [concat [get_pins -leaf -of_objects $nets -filter {DIRECTION == OUT}] [get_ports -of_objects $nets -filter {DIRECTION == IN}]]]
    lappend terms "[get_property REF_PIN_NAME $ip]=[join $drivers ,]"
  }
  puts $f "$c\t$kind\t[get_property INIT $c]\t[join $terms ;]"
}
close $f
quit
