# usage: vivado -mode batch -source keep.tcl -tclargs <dcp> <out.txt>
# Record whether the protocol wrapper cell carries KEEP_HIERARCHY in the checkpoint.
lassign $argv dcp out
set_param general.maxThreads 2
open_checkpoint $dcp
set fh [open $out w]
set c [get_cells milan_datapath/pp_shadow]
puts $fh "cell\t$c"
puts $fh "KEEP_HIERARCHY\t[get_property KEEP_HIERARCHY $c]"
puts $fh "IS_PRIMITIVE\t[get_property IS_PRIMITIVE $c]"
puts $fh "ORIG_REF_NAME\t[get_property ORIG_REF_NAME $c]"
close $fh
quit
