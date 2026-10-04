# SPDX-License-Identifier: CERN-OHL-W-2.0
# Standalone out-of-context synthesis of KL_srp_top (reviewer probe, not
# the #638 recipe; mirrors HANDOFF 4.3: wrapper tying req_max_interval_i
# to 1, AreaOptimized_high, 20 ns): base and head, 2/2 (SLOT_AW_P 6) and 9/9 (SLOT_AW_P 7).
# usage: vivado -mode batch -source srp_ooc.tcl -tclargs OUT_DIR BASE_HDL HEAD_HDL
set out  [lindex $argv 0]
set base [lindex $argv 1]
set head [lindex $argv 2]
set_param general.maxThreads 8
set mods {KL_srp_decoder KL_srp_domain KL_srp_vlan KL_srp_talker_fsm KL_srp_listener_fsm KL_srp_admission KL_srp_encoder KL_srp_top}
foreach combo {{base 2 6} {head 2 6} {base 9 7} {head 9 7}} {
  lassign $combo which n aw
  set hdl [expr {$which eq "base" ? $base : $head}]
  set tag "$which-${n}x${n}"
  file mkdir $out/$tag
  close_project -quiet
  create_project -in_memory -part xc7a100tfgg484-2
  read_verilog -sv [list $hdl/common/pp_pkg.sv $hdl/srp/srp_pkg.sv]
  foreach m $mods { read_verilog -sv $hdl/srp/$m.sv }
  read_verilog -sv [file dirname [info script]]/srp_area_wrap.sv
  read_xdc [file dirname [info script]]/srp_ooc.xdc
  synth_design -top srp_area_wrap -part xc7a100tfgg484-2 -mode out_of_context \
    -directive AreaOptimized_high -flatten_hierarchy rebuilt \
    -generic N_P=$n -generic AW_P=$aw
  report_utilization -file $out/$tag/util.rpt
  report_utilization -hierarchical -file $out/$tag/util_hier.rpt
  report_ram_utilization -file $out/$tag/ram.rpt
  # flip-flop census of the storage this change moves
  set fh [open $out/$tag/census.tsv w]
  foreach pat {tf_ram_r tf_tk_ram_r tf_ls_ram_r tf_q_r wtsp_r wid_r wsid_r slope_q_r mfs_r mif_r prio_r rank_r lat_r sid_r} {
    set ff  [llength [get_cells -quiet -hier -filter "PRIMITIVE_GROUP == FLOP_LATCH && NAME =~ *${pat}_reg*"]]
    set ram [llength [get_cells -quiet -hier -filter "PRIMITIVE_GROUP == DISTRIBUTED_MEMORY && NAME =~ *${pat}_reg*"]]
    set bram [llength [get_cells -quiet -hier -filter "PRIMITIVE_GROUP == BLOCKRAM && NAME =~ *${pat}*"]]
    puts $fh "$pat\t$ff\t$ram\t$bram"
  }
  puts $fh "ALL_BRAM\t[llength [get_cells -quiet -hier -filter {PRIMITIVE_GROUP == BLOCKRAM}]]\t[join [get_cells -quiet -hier -filter {PRIMITIVE_GROUP == BLOCKRAM}] ,]"
  close $fh
}
puts "SRP_OOC DONE"
