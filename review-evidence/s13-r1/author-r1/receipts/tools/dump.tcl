# dump.tcl <route.dcp> <out-prefix>: a routed checkpoint as three sorted text files, for a line diff between two images:
#   <out>.cells   every primitive cell: name, REF_NAME, LOC, BEL, and each INIT* property it carries
#   <out>.nets    every top-level signal net's ROUTE (its physical route, the PIPs it uses)
#   <out>.summary the cell, net and routing counts
set dcp [lindex $argv 0]; set out [lindex $argv 1]
open_checkpoint $dcp
set f [open $out.cells w]
set ncell 0
foreach c [get_cells -hierarchical -filter {IS_PRIMITIVE}] {
  set ref [get_property REF_NAME $c]
  set line "$c $ref [get_property LOC $c] [get_property BEL $c]"
  foreach p [lsort [list_property $c INIT*]] {
    append line " $p=[get_property $p $c]"
  }
  puts $f $line
  incr ncell
}
close $f
set f [open $out.nets w]
set nnet 0
foreach n [get_nets -hierarchical -top_net_of_hierarchical_group -filter {TYPE != POWER && TYPE != GROUND}] {
  puts $f "$n [get_property ROUTE $n]"
  incr nnet
}
close $f
set f [open $out.summary w]
puts $f "cells $ncell nets $nnet"
puts $f [report_route_status -return_string]
close $f
