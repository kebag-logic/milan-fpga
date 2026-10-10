# R590-2: out-of-context synthesis of one emitted lane-test bench (every
# framing flag a port). Usage:
#   vivado -mode batch -nojournal -log <tag>.log -source ooc_bench.tcl -tclargs <bench.v> <outdir> <tag>
set bench [lindex $argv 0]
set out   [lindex $argv 1]
set tag   [lindex $argv 2]
read_verilog $bench
synth_design -top bench -part xc7a100tfgg484-2 -mode out_of_context -directive AreaOptimized_high
report_utilization -file $out/$tag.util.rpt
set f [open $out/$tag.cells.txt w]
foreach c [lsort [get_cells -hier -filter {PRIMITIVE_GROUP == BLOCKRAM || PRIMITIVE_GROUP == DMEM}]] {
  puts $f "[get_property REF_NAME $c] $c"
}
close $f
