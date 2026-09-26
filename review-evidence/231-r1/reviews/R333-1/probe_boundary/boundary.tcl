# usage: vivado -mode batch -source boundary.tcl -tclargs <synth.dcp> <out.tsv>
# For each scope, count its LUTs by where their loads and drivers sit
# relative to the protocol wrapper (milan_datapath/pp_shadow).
lassign $argv dcp out
set_param general.maxThreads 2
open_checkpoint $dcp
set wrap milan_datapath/pp_shadow
set fh [open $out w]
puts $fh "scope\tLUT\tLUT_all_loads_outside_wrapper\tLUT_any_load_outside_wrapper\tLUT_any_input_from_outside_wrapper\tLUT_outside_input_and_only_outside_loads"
foreach scope [list $wrap/u_pp/u_aecp/u_dyn $wrap/u_pp/u_aecp $wrap/u_pp/u_srp $wrap/u_pp/u_notify $wrap] {
  set luts [get_cells -hier -filter [format {NAME =~ "%s/*" && REF_NAME =~ "LUT*"} $scope]]
  set all_out 0; set any_out 0; set any_in 0; set both 0
  foreach l $luts {
    set onet [get_nets -of_objects [get_pins -of_objects $l -filter {DIRECTION == OUT}]]
    set loads [get_cells -quiet -of_objects [get_pins -quiet -leaf -of_objects $onet -filter {DIRECTION == IN}]]
    set outside 0; set inside 0
    foreach c $loads { if {[string first "$wrap/" $c] == 0} { incr inside } else { incr outside } }
    if {$outside > 0} { incr any_out; if {$inside == 0} { incr all_out } }
    set ext 0
    foreach p [get_pins -of_objects $l -filter {DIRECTION == IN}] {
      set drv [get_cells -quiet -of_objects [get_pins -quiet -leaf -of_objects [get_nets -of_objects $p] -filter {DIRECTION == OUT}]]
      foreach c $drv { if {[string first "$wrap/" $c] != 0} { set ext 1 } }
    }
    incr any_in $ext
    if {$ext && $outside > 0 && $inside == 0} { incr both }
  }
  puts $fh "$scope\t[llength $luts]\t$all_out\t$any_out\t$any_in\t$both"
  flush $fh
}
close $fh
quit
