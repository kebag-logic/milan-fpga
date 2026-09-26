# usage: vivado -mode batch -source keep_prop.tcl -tclargs <dcp> <out.txt>
# Record the wrapper cell's KEEP_HIERARCHY / DONT_TOUCH properties and whether
# any primitive whose name is outside the wrapper has ORIG_REF_NAME under it.
lassign $argv dcp out
set_param general.maxThreads 2
open_checkpoint $dcp
set fh [open $out w]
set pp [get_cells milan_datapath/pp_shadow]
puts $fh "cell\t$pp"
foreach p {KEEP_HIERARCHY DONT_TOUCH IS_PRIMITIVE ORIG_REF_NAME REF_NAME} {
  puts $fh "$p\t[get_property -quiet $p $pp]"
}
puts $fh "wrapper_primitives\t[llength [get_cells -hier -filter {NAME =~ milan_datapath/pp_shadow/* && IS_PRIMITIVE == 1}]]"
puts $fh "wrapper_LUTs\t[llength [get_cells -hier -filter {NAME =~ milan_datapath/pp_shadow/* && REF_NAME =~ LUT*}]]"
close $fh
quit
