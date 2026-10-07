if {[llength $argv] != 2} { error "Usage: shared-logic.tcl <head-route.dcp> <base-route.dcp>" }
set_param general.maxThreads 1
foreach tag {base head} {
  if {$tag eq "base"} { set dcp [lindex $argv 1] } else { set dcp [lindex $argv 0] }
  open_checkpoint $dcp
  set roots [get_cells -hier -filter {NAME =~ *src_band_ticks_r* && REF_NAME =~ LUT*}]
  set inputs [get_pins -of_objects $roots -filter {DIRECTION == IN}]
  set cone [concat $roots [all_fanin -flat -only_cells -to $inputs] [get_cells -hier -filter {REF_NAME == VCC || REF_NAME == GND}]]
  set f [open $tag.shared_logic.tsv w]
  foreach c [lsort -unique $cone] {
    set kind [get_property REF_NAME $c]
    if {![string match LUT* $kind] && $kind ne "CARRY4" && $kind ne "GND" && $kind ne "VCC" && ![string match FD* $kind]} { continue }
    set init -
    if {[string match LUT* $kind]} { set init [get_property INIT $c] }
    set terms {}
    foreach ip [lsort [get_pins -of_objects $c -filter {DIRECTION == IN}]] {
      set nets [get_nets -of_objects $ip]
      set drivers [lsort [concat [get_pins -quiet -leaf -of_objects $nets -filter {DIRECTION == OUT}] [get_ports -quiet -of_objects $nets -filter {DIRECTION == IN}]]]
      lappend terms "[get_property REF_PIN_NAME $ip]=[join $drivers ,]"
    }
    puts $f "$c\t$kind\t$init\t[join $terms {;}]"
  }
  close $f
  close_design
}
quit
