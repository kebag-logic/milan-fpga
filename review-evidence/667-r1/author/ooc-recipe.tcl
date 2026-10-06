set_param general.maxThreads 16
rename synth_design synth_design_original
proc synth_design {args} {
  set p [lsearch -exact $args -include_dirs]
  if {$p < 0} { error "missing include directories" }
  set incs [lindex $args [expr {$p+1}]]
  set incs [lreplace $incs 0 0 "$::env(LANE_ROOT)/configs/generated/endstation_ax7101_1x1_tdm8"]
  set args [lreplace $args [expr {$p+1}] [expr {$p+1}] $incs]
  foreach g {N_STREAMS=1 TALKER_WIRE_CHANS_P=8 AUDIO_IF_SLOTS_P=8 AUDIO_IF_MASTER_P=1 AUDIO_IF_RENDER_SLOTS_P=8 LOOPBACK_P=1 I2SPB_P=0 LPF_P=0 MILAN_CLK_FREQ_HZ=50000000} {
    lappend args -generic $g
  }
  puts "MEASURED_SYNTH_ARGS $args"
  synth_design_original {*}$args
}
source "$::env(LANE_ROOT)/syn/ooc/milan_datapath_ooc.tcl"
