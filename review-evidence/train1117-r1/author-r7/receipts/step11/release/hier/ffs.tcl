# ffs.tcl: flops (and replicas) per instance whose RTL is unchanged but whose flop count moved; the datapath's own.
foreach {tag dcp} $argv {
  open_checkpoint $dcp
  set fh [open ffs-$tag.txt w]
  foreach inst {milan_datapath/ptp_clock_validity milan_datapath/avtp_rx_monitor milan_datapath/g_aaf_meter.aaf_clock_meter milan_datapath/g_tdm_render_live.g_master.chan_tdm_render} {
    set all [get_cells -hier -quiet -filter "IS_PRIMITIVE && PRIMITIVE_GROUP == FLOP_LATCH && NAME =~ $inst/*"]
    set rep [get_cells -hier -quiet -filter "IS_PRIMITIVE && PRIMITIVE_GROUP == FLOP_LATCH && NAME =~ $inst/* && NAME =~ *replica*"]
    puts $fh "$inst: [llength $all] flops, [llength $rep] named *replica*"
  }
  set own [get_cells -quiet -filter {IS_PRIMITIVE && PRIMITIVE_GROUP == FLOP_LATCH} milan_datapath/*]
  set stems [dict create]
  foreach c $own { regsub {(_reg)?(\[[0-9]+\])*(_replica(_[0-9]+)?)?$} [get_property NAME $c] {} s; dict incr stems $s }
  puts $fh "milan_datapath own flops: [llength $own]"
  foreach k [lsort [dict keys $stems]] { puts $fh "  $k [dict get $stems $k]" }
  close $fh
  close_design
}
