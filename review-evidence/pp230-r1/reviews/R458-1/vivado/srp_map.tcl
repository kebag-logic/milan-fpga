# SPDX-License-Identifier: CERN-OHL-W-2.0
# R458-1 probe: out-of-context synthesis of KL_srp_top alone to read how each
# SRP memory maps (distributed RAM, block RAM or flip-flops). Not the #638
# recipe and not a resource figure for the product; a mapping check only.
# usage: vivado -mode batch -source srp_map.tcl -tclargs <tree> <N> <SLOT_AW> <out>
lassign $argv tree n aw out
file mkdir $out
set hdl $tree/hdl
read_verilog -sv [list $hdl/common/pp_pkg.sv $hdl/srp/srp_pkg.sv \
  $hdl/srp/KL_srp_decoder.sv $hdl/srp/KL_srp_domain.sv $hdl/srp/KL_srp_vlan.sv \
  $hdl/srp/KL_srp_talker_fsm.sv $hdl/srp/KL_srp_listener_fsm.sv \
  $hdl/srp/KL_srp_admission.sv $hdl/srp/KL_srp_encoder.sv $hdl/srp/KL_srp_top.sv]
synth_design -top KL_srp_top -part xc7a100tfgg484-2 -mode out_of_context \
  -directive AreaOptimized_high -flatten_hierarchy rebuilt \
  -generic N_SOURCES_P=$n -generic N_SINKS_P=$n -generic SLOT_AW_P=$aw
report_utilization -hierarchical -file $out/util_hier.rpt
report_utilization -file $out/util.rpt
report_ram_utilization -detail -file $out/ram.rpt
set fh [open $out/ram_cells.txt w]
foreach c [lsort [get_cells -hier -filter {PRIMITIVE_GROUP == BLOCKRAM || PRIMITIVE_GROUP == DMEM}]] {
  puts $fh "[get_property REF_NAME $c] $c"
}
close $fh
set fh [open $out/ff_on_memories.txt w]
foreach pat {*tf_ram_r* *tf_tk_ram_r* *tf_ls_ram_r* *wtsp_r* *wid_r* *wsid_r* *slope_q_r* *mfs_r* *mif_r* *lat_r_reg*} {
  puts $fh "$pat [llength [get_cells -hier -quiet -filter "PRIMITIVE_GROUP == FLOP_LATCH && NAME =~ $pat"]]"
}
close $fh
