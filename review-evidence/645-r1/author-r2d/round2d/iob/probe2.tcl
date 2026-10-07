set dcp [lindex $argv 0]
open_checkpoint $dcp
set f [get_cells milansoc_phy_source_valid_reg]
foreach p [get_pins -of_objects $f] {
  set n [get_nets -quiet -of_objects $p]
  set drv [get_cells -quiet -of_objects [get_pins -quiet -of_objects $n -filter {DIRECTION == OUT}]]
  puts "PROBE ff pin: [get_property REF_PIN_NAME $p] net: $n driver: $drv [get_property -quiet REF_NAME $drv]"
}
set l [get_cells -quiet milansoc_phy_source_valid_i_1]
if {[llength $l]} {
  puts "PROBE lut INIT: [get_property INIT $l]"
  foreach p [get_pins -of_objects $l -filter {DIRECTION == IN}] {
    set n [get_nets -of_objects $p]
    set drv [get_cells -quiet -of_objects [get_pins -quiet -of_objects $n -filter {DIRECTION == OUT}]]
    puts "PROBE lut pin: [get_property REF_PIN_NAME $p] net: $n driver: $drv [get_property -quiet REF_NAME $drv] fanout: [llength [get_pins -of_objects $n -filter {DIRECTION == IN}]]"
  }
}
close_design
