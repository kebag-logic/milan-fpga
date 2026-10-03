# Scratch probe (never committed). For each named register structure in a
# synthesized checkpoint: its flip-flops; the LUTs of its read cone (all_fanout
# to the next sequential endpoints) inside its own module; and the "exclusive"
# LUTs among those, whose every input is the structure or another exclusive
# LUT (a pure read function of the structure, the part a RAM read replaces).
#   vivado -mode batch -source cone_probe.tcl -tclargs <checkpoint> <out.tsv>
set_param general.maxThreads 8
open_checkpoint [lindex $argv 0]
set out [open [lindex $argv 1] w]
puts $out "structure\tFF\tcone_LUT_in_module\tcone_MUXF_in_module\texclusive_LUT\texclusive_MUXF\twrite_cone_LUT_in_module"
foreach {name pattern scope} {
  notify_rows_r        u_pp/u_notify/rows_r_reg*      u_pp/u_notify
  notify_ctr_last_r    u_pp/u_notify/ctr_last_r_reg*  u_pp/u_notify
  srp_tf_ram_r         u_pp/u_srp/tf_ram_r_reg*       u_pp/u_srp
  top_armq_r           u_pp/armq_r_reg*               u_pp
  top_bound            u_pp/bound_*_r_reg*            u_pp
  srp_talker_ctx       u_pp/u_srp/u_talker/*_r_reg*   u_pp/u_srp/u_talker
  srp_listener_ctx     u_pp/u_srp/u_listener/*_r_reg* u_pp/u_srp/u_listener
} {
  set regs [get_cells -quiet -hier -filter "IS_SEQUENTIAL == 1 && NAME =~ $pattern"]
  set nff [llength $regs]
  if {$nff == 0} { puts $out "$name\t0\t0\t0\t0\t0\t0"; continue }
  set q [get_pins -of_objects $regs -filter {REF_PIN_NAME == Q}]
  set cone [all_fanout -from $q -flat -only_cells]
  set local {}
  foreach c $cone {
    set n [get_property NAME $c]
    if {[string first "$scope/" $n] == 0 && [string first "/" [string range $n [expr {[string length $scope] + 1}] end]] < 0} {
      lappend local $c
    }
  }
  set luts [filter -quiet $local {REF_NAME =~ LUT* || REF_NAME =~ MUXF*}]
  set member [dict create]
  foreach r $regs { dict set member [get_property NAME $r] 1 }
  # Iterate to a fixed point: a cell is exclusive when every input driver is a member.
  set changed 1
  while {$changed} {
    set changed 0
    foreach c $luts {
      set n [get_property NAME $c]
      if {[dict exists $member $n]} { continue }
      set ok 1
      foreach p [get_pins -quiet -of_objects $c -filter {DIRECTION == IN}] {
        set drv [get_cells -quiet -of_objects [get_pins -quiet -leaf -filter {DIRECTION == OUT} -of_objects [get_nets -quiet -of_objects $p]]]
        if {[llength $drv] != 1 || ![dict exists $member [get_property NAME $drv]]} { set ok 0; break }
      }
      if {$ok} { dict set member $n 1; set changed 1 }
    }
  }
  set nl 0; set nm 0; set el 0; set em 0
  foreach c $luts {
    set ref [get_property REF_NAME $c]
    set ex [dict exists $member [get_property NAME $c]]
    if {[string match LUT* $ref]} { incr nl; if {$ex} { incr el } } else { incr nm; if {$ex} { incr em } }
  }
  set d [get_pins -of_objects $regs -filter {REF_PIN_NAME == D || REF_PIN_NAME == CE || REF_PIN_NAME == R}]
  set fin [all_fanin -to $d -flat -only_cells]
  set wl 0
  foreach c [filter -quiet $fin {REF_NAME =~ LUT*}] {
    if {[string first "$scope/" [get_property NAME $c]] == 0} { incr wl }
  }
  puts $out "$name\t$nff\t$nl\t$nm\t$el\t$em\t$wl"
  flush $out
}
close $out
quit
