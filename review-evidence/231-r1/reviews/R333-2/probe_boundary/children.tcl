# usage: vivado -mode batch -source children.tcl -tclargs <dcp> <wrapper-path> <out.tsv>
# List every direct hierarchical child of the wrapper and of <wrapper>/u_pp in
# the netlist, with its leaf-primitive count, to check ranking completeness.
lassign $argv dcp wrap out
set_param general.maxThreads 2
open_checkpoint $dcp
set fh [open $out w]
puts $fh "parent\tchild\tprimitives"
foreach parent [list $wrap $wrap/u_pp] {
  foreach c [lsort [get_cells -quiet -filter {IS_PRIMITIVE == 0} $parent/*]] {
    set n [llength [get_cells -quiet -hier -filter [format {NAME =~ "%s/*" && IS_PRIMITIVE == 1} $c]]]
    puts $fh "$parent\t[string range $c [expr {[string length $parent] + 1}] end]\t$n"
  }
  set own [llength [get_cells -quiet -filter {IS_PRIMITIVE == 1} $parent/*]]
  puts $fh "$parent\t@own\t$own"
}
close $fh
quit
