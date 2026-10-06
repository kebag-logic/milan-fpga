# scratch: OOC synthesis of the option prototypes and their baselines
# xc7a100tfgg484-2 (AX7101), 20 ns (the shipping 50 MHz axis clock)
set PART xc7a100tfgg484-2
set CMC_G {N_SLOTS_P=4 N_TDM_P=8 TDM_FRAME_PAIRS_P=4 N_LB_STREAMS_P=1 N_LB_CH_P=8}
set CFGS [list \
  [list settle_base settle_base {settle_base.sv} {} {axis_clk}] \
  [list settle_optB settle_optB {settle_optB.sv} {} {axis_clk}] \
  [list settle_optC settle_optC {settle_optC.sv} {} {axis_clk}] \
  [list cmc_base KL_chan_map_capture {cmc_base.sv} $CMC_G {clk_i}] \
  [list cmc_rc KL_chan_map_capture_rc {cmc_rc.sv} $CMC_G {clk_i}] \
  [list servo_base KL_mmcm_drp_servo {cdc_pulse.sv cdc_handshake.sv servo_base.sv} {} {clk_i clk_audio_i ps_clk_i}] \
  [list servo_ph KL_mmcm_drp_servo_ph {cdc_pulse.sv cdc_handshake.sv servo_ph.sv} {} {clk_i clk_audio_i ps_clk_i}] \
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
  set p 20.000
  foreach k $clks {
    if {$k eq "clk_audio_i"} { set pp 40.690 } elseif {$k eq "ps_clk_i"} { set pp 5.000 } else { set pp $p }
    puts $fh "create_clock -period $pp -name $k \[get_ports $k\]"
  }
  if {[llength $clks] > 1} { puts $fh "set_clock_groups -asynchronous [join [lmap k $clks {format {-group [get_clocks %s]} $k}] { }]" }
  close $fh
  read_xdc -mode out_of_context $xdc
  synth_design -top $top -part $PART -mode out_of_context -include_dirs [pwd] {*}$gargs
  report_utilization -file util_$tag.rpt
  report_utilization -hierarchical -file util_hier_$tag.rpt
  close_design
  remove_files [get_files -quiet *]
}
puts "=== OOC ALL DONE"
