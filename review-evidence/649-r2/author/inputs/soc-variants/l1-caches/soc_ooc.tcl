# Scratch only: Vivado out-of-context synthesis of one exported SoC top (issue #649 round 2).
set dir [file normalize [lindex $argv 0]]
cd $dir
set fh [open sources.txt r]; set sources [split [string trim [read $fh]] "\n"]; close $fh
foreach source $sources { read_verilog $source }
synth_design -directive default -mode out_of_context -top alinx_ax7101 -part xc7a100t-fgg484-2
report_utilization -hierarchical -hierarchical_depth 2 -file synth_hierarchy.rpt
report_utilization -file synth_utilization.rpt
# No opt_design: it refuses primitives that a black box drives (Opt 31-30), and the black boxes are the
# point of this run. Every variant is therefore compared after synthesis.
puts "SOC_OOC_DONE"
