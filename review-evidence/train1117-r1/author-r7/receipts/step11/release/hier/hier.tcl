# hier.tcl: the release image's routed checkpoints (ExtraPostPlacementOpt), the candidate c8ff391a's and p11's:
# report_utilization -hierarchical, and each cdc_pair_fifo instance's primitives by type.
set_param general.maxThreads 8
foreach {tag dcp} $argv {
  open_checkpoint $dcp
  report_utilization -hierarchical -hierarchical_depth 24 -file hier-$tag.rpt
  report_utilization -file util-$tag.rpt
  set fh [open prims-$tag.txt w]
  foreach inst [lsort [get_cells -hier -quiet -filter {ORIG_REF_NAME =~ cdc_pair_fifo* || REF_NAME =~ cdc_pair_fifo*}]] {
    set counts [dict create]
    foreach c [get_cells -hier -quiet -filter "NAME =~ $inst/* && IS_PRIMITIVE"] {
      dict incr counts [get_property REF_NAME $c]
    }
    set line "$inst ([get_property REF_NAME [get_cells $inst]])"
    foreach k [lsort [dict keys $counts]] { append line " $k:[dict get $counts $k]" }
    puts $fh $line
  }
  close $fh
  close_design
}
