# bramdump.tcl <route.dcp> <out>: every block RAM cell of a routed checkpoint, one line each: name, LOC and every
# INIT* property (INIT_00..7F, INITP_00..0F, INIT_A/B, ...), sorted; for a diff of two images' memory contents.
set dcp [lindex $argv 0]; set out [lindex $argv 1]
open_checkpoint $dcp
set f [open $out w]
foreach c [lsort [get_cells -hierarchical -filter {IS_PRIMITIVE && REF_NAME =~ RAMB*}]] {
  set line "$c [get_property REF_NAME $c] [get_property LOC $c]"
  foreach p [lsort [list_property $c INIT*]] { append line " $p=[get_property $p $c]" }
  puts $f $line
}
close $f
