# usage: vivado -mode batch -source loads.tcl -tclargs <synth.dcp> <scope> <out.tsv>
# Histogram of the sequential/primitive load stems (indices stripped) reached
# by LUTs under <scope> whose loads are all outside milan_datapath/pp_shadow.
lassign $argv dcp scope out
set_param general.maxThreads 2
open_checkpoint $dcp
set wrap milan_datapath/pp_shadow
array set hist {}
foreach l [get_cells -hier -filter [format {NAME =~ "%s/*" && REF_NAME =~ "LUT*"} $scope]] {
  set onet [get_nets -of_objects [get_pins -of_objects $l -filter {DIRECTION == OUT}]]
  set loads [get_cells -quiet -of_objects [get_pins -quiet -leaf -of_objects $onet -filter {DIRECTION == IN}]]
  set inside 0
  foreach c $loads { if {[string first "$wrap/" $c] == 0} { set inside 1 } }
  if {$inside || [llength $loads] == 0} { continue }
  foreach c $loads {
    regsub -all {\[[0-9]+\]} $c {[]} stem
    regsub -all {_i_[0-9]+(__[0-9]+)?$} $stem {_i_*} stem
    if {[info exists hist($stem)]} { incr hist($stem) } else { set hist($stem) 1 }
  }
}
set fh [open $out w]
foreach k [lsort [array names hist]] { puts $fh "$hist($k)\t$k" }
close $fh
quit
