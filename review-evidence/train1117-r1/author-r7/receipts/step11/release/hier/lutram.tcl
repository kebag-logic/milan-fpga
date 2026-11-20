# lutram.tcl: every distributed-RAM and block-RAM primitive in milan_datapath's own cells and under u_fcdc, by name
# stem, in each routed release checkpoint; and every primitive whose name holds u_fcdc, wherever its parent.
foreach {tag dcp} $argv {
  open_checkpoint $dcp
  set fh [open lutram-$tag.txt w]
  set stems [dict create]
  foreach c [get_cells -hier -quiet -filter {IS_PRIMITIVE && (PRIMITIVE_GROUP == DMEM || PRIMITIVE_GROUP == BLOCKRAM)}] {
    set n [get_property NAME $c]
    if {![string match *u_fcdc* $n] && ![string match milan_datapath/* $n]} continue
    regsub {_[0-9]+_[0-9]+(_[0-9]+_[0-9]+)?(/[A-Z0-9_]+)?$} $n {*} stem
    dict incr stems "[get_property REF_NAME $c] $stem"
  }
  foreach k [lsort [dict keys $stems]] { if {[string match *fcdc* $k] || [string match *tdm_render* $k]} { puts $fh "$k: [dict get $stems $k]" } }
  puts $fh "u_fcdc-named primitives by type:"
  set t [dict create]
  foreach c [get_cells -hier -quiet -filter {IS_PRIMITIVE && NAME =~ *u_fcdc*}] { dict incr t [get_property REF_NAME $c] }
  foreach k [lsort [dict keys $t]] { puts $fh "  $k [dict get $t $k]" }
  set ex [lindex [get_cells -hier -quiet -filter {IS_PRIMITIVE && NAME =~ *u_fcdc* && REF_NAME =~ RAM*}] 0]
  if {$ex ne ""} { puts $fh "example: $ex parent [get_property PARENT $ex]" }
  close $fh
  close_design
}
