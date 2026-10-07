# Read-only: what reads eth0_rx_dv's input buffer, and the phy_source_valid flop.
set dcp [lindex $argv 0]
open_checkpoint $dcp
set port [get_ports eth0_rx_dv]
set pnet [get_nets -of_objects $port]
puts "PROBE port net: $pnet"
foreach c [get_cells -of_objects $pnet] { puts "PROBE pad cell: $c [get_property REF_NAME $c]" }
foreach b [get_cells -of_objects $pnet -filter {REF_NAME =~ IBUF*}] {
  foreach o [get_pins -of_objects $b -filter {DIRECTION == OUT}] {
    set n [get_nets -of_objects $o]
    puts "PROBE ibuf out net: $n"
    foreach l [get_pins -of_objects $n -filter {DIRECTION == IN}] {
      set lc [get_cells -of_objects $l]
      puts "PROBE load: $l [get_property REF_NAME $lc]"
    }
  }
}
foreach c [get_cells -hier -filter {NAME =~ *phy_source_valid*}] {
  set d [get_pins -quiet $c/D]
  set drv {}
  if {[llength $d]} { set drv [get_cells -of_objects [get_pins -of_objects [get_nets -of_objects $d] -filter {DIRECTION == OUT}]] }
  puts "PROBE flop: $c [get_property REF_NAME $c] D-driver: $drv [get_property -quiet REF_NAME $drv]"
}
close_design
