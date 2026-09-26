# usage: vivado -mode batch -source feedthrough.tcl -tclargs <dcp> <scope> <out.tsv>
# For LUTs under <scope> that have an input driven from outside the wrapper and
# only loads outside it, histogram the wrapper boundary pins (port stems) on
# their input and output nets: a genuine wrapper feed-through crosses an input
# port and an output port of milan_datapath/pp_shadow.
lassign $argv dcp scope out
set_param general.maxThreads 2
open_checkpoint $dcp
set wrap milan_datapath/pp_shadow
array set hin {}; array set hout {}
set n 0
foreach l [get_cells -hier -filter [format {NAME =~ "%s/*" && REF_NAME =~ "LUT*"} $scope]] {
  set onet [get_nets -of_objects [get_pins -of_objects $l -filter {DIRECTION == OUT}]]
  set loads [get_cells -quiet -of_objects [get_pins -quiet -leaf -of_objects $onet -filter {DIRECTION == IN}]]
  set inside 0
  foreach c $loads { if {[string first "$wrap/" $c] == 0} { set inside 1 } }
  if {$inside || [llength $loads] == 0} { continue }
  set ext 0; set inpins {}
  foreach p [get_pins -of_objects $l -filter {DIRECTION == IN}] {
    set net [get_nets -of_objects $p]
    set drv [get_cells -quiet -of_objects [get_pins -quiet -leaf -of_objects $net -filter {DIRECTION == OUT}]]
    foreach c $drv { if {[string first "$wrap/" $c] != 0} { set ext 1 } }
    foreach bp [get_pins -quiet -of_objects [get_nets -quiet -segments $net] -filter [format {NAME =~ "%s/*" && IS_LEAF == 0} $wrap]] {
      if {[regexp "^$wrap/\[^/\]+$" $bp]} { lappend inpins $bp }
    }
  }
  if {!$ext} { continue }
  incr n
  foreach bp [lsort -unique $inpins] {
    regsub -all {\[[0-9]+\]} $bp {[]} s
    if {[info exists hin($s)]} { incr hin($s) } else { set hin($s) 1 }
  }
  foreach bp [get_pins -quiet -of_objects [get_nets -quiet -segments $onet] -filter [format {NAME =~ "%s/*" && IS_LEAF == 0} $wrap]] {
    if {[regexp "^$wrap/\[^/\]+$" $bp]} {
      regsub -all {\[[0-9]+\]} $bp {[]} s
      if {[info exists hout($s)]} { incr hout($s) } else { set hout($s) 1 }
    }
  }
}
set fh [open $out w]
puts $fh "cells\t$n"
foreach k [lsort [array names hin]] { puts $fh "in\t$hin($k)\t$k\t[get_property DIRECTION [get_pins [string map {{[]} {[0]}} $k]]]" }
foreach k [lsort [array names hout]] { puts $fh "out\t$hout($k)\t$k\t[get_property DIRECTION [get_pins [string map {{[]} {[0]}} $k]]]" }
close $fh
quit
