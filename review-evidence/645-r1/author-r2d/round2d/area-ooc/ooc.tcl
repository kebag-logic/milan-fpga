# Base and depth-sixteen candidate, shipping 1x1 shape, 20 ns axis clock.
# One configuration per vendor process under the shared lock.
set PART xc7a100tfgg484-2
set CMC_G {N_SLOTS_P=4 N_TDM_P=8 TDM_FRAME_PAIRS_P=4 N_LB_STREAMS_P=1 N_LB_CH_P=8}
set CFGS [list \
  [list settle_base settle_base {settle_base.sv} {} {axis_clk}] \
  [list settle_head settle_new {settle_new.sv} {} {axis_clk}] \
  [list cmc_base KL_chan_map_capture {cmc_base.sv} $CMC_G {clk_i}] \
  [list cmc_head KL_chan_map_capture {cmc_head.sv} $CMC_G {clk_i}] \
]
set sel {}
if {[info exists ::env(ONLY)] && $::env(ONLY) ne ""} { set sel [split $::env(ONLY) ,] }
foreach c $CFGS {
  lassign $c tag top files gens clks
  if {[llength $sel] && [lsearch -exact $sel $tag] < 0} continue
  puts "=== OOC $tag ($top)"
  foreach f $files { read_verilog -sv $f }
  set gargs {}
  foreach g $gens { lappend gargs -generic $g }
  set xdc "xdc_$tag.xdc"
  set fh [open $xdc w]
  foreach k $clks { puts $fh "create_clock -period 20.000 -name $k \[get_ports $k\]" }
  close $fh
  read_xdc -mode out_of_context $xdc
  synth_design -top $top -part $PART -mode out_of_context -include_dirs [pwd] {*}$gargs
  report_utilization -file util_$tag.rpt
  report_utilization -hierarchical -file util_hier_$tag.rpt
  report_timing_summary -max_paths 3 -file timing_$tag.rpt
  set f [open ffs_$tag.txt w]
  foreach r [get_cells -hier -filter {IS_PRIMITIVE && PRIMITIVE_GROUP == FLOP_LATCH}] { puts $f $r }
  close $f
  set f [open cells_$tag.tsv w]
  foreach c [get_cells -hier -filter {IS_PRIMITIVE}] { puts $f "$c\t[get_property REF_NAME $c]" }
  close $f
  close_design
}
puts "=== OOC ALL DONE"
