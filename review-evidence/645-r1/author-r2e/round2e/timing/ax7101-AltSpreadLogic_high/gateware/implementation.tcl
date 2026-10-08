set_param general.maxThreads 32
open_checkpoint {$WORK/timing/ax7101/gateware/alinx_ax7101_synth.dcp}
# Add pre-optimize commands

source {$WORK/functional/route/sw/litex/clock_constraints.tcl}
kl_quasi_static_constraints
milan_eth_constraints eth_clocks0_rx [list milansoc_crg_clkout0 milansoc_crg_clkout1] [list milansoc_crg_pll_audio_fb milansoc_crg_audio_ref_raw milansoc_crg_audio_mclk_raw milansoc_crg_clkout2 milansoc_crg_clkout3 milansoc_crg_clkout4]

# Optimize design

opt_design -directive ExploreArea

# Add pre-placement commands

source {$WORK/functional/route/sw/litex/timing_grade.tcl}
kl_timing_grade_configure {xc7a100t-fgg484-2} {commercial} {0} {85} {Slow Fast}

# Placement

place_design -directive AltSpreadLogic_high
phys_opt_design -directive AggressiveExplore

# Placement report

report_utilization -hierarchical -file alinx_ax7101_utilization_hierarchical_place.rpt
report_utilization -file alinx_ax7101_utilization_place.rpt
report_io -file alinx_ax7101_io.rpt
report_control_sets -verbose -file alinx_ax7101_control_sets.rpt
report_clock_utilization -file alinx_ax7101_clock_utilization.rpt
write_checkpoint -force alinx_ax7101_place.dcp

# Add pre-routing commands

source {$WORK/functional/route/sw/litex/iob_pack_check.tcl}
kl_iob_pack_check alinx_ax7101_iob_pack.rpt

# Routing

route_design -directive AggressiveExplore
phys_opt_design -directive AggressiveExplore
write_checkpoint -force alinx_ax7101_route.dcp

# Routing report

report_timing_summary -no_header -no_detailed_paths
report_route_status -file alinx_ax7101_route_status.rpt
report_drc -file alinx_ax7101_drc.rpt
report_timing_summary -datasheet -max_paths 10 -file alinx_ax7101_timing.rpt
report_power -file alinx_ax7101_power.rpt
kl_timing_grade_reports alinx_ax7101_signoff
set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
set_property CONFIG_MODE SPIx4 [current_design]
set_property BITSTREAM.CONFIG.CONFIGRATE 50 [current_design]
set_property CFGBVS VCCO [current_design]
set_property CONFIG_VOLTAGE 3.3 [current_design]
report_clock_interaction -delay_type min_max -file alinx_ax7101_clock_interaction.rpt
report_exceptions -file alinx_ax7101_exceptions.rpt


report_utilization -hierarchical -hierarchical_depth 10 -hierarchical_min_primitive_count 0 -file baseline_hierarchy.rpt
report_utilization -file baseline_utilization.rpt
report_timing_summary -max_paths 10 -file baseline_timing.rpt
set pf [open baseline_cells.tsv w]
puts $pf "cell\tprimitive"
foreach c [get_cells -hier -filter {IS_PRIMITIVE == 1}] {
  puts $pf "$c\t[get_property REF_NAME $c]"
}
close $pf

set pp [get_cells -hier -filter {ORIG_REF_NAME == KL_pp_shadow || REF_NAME == KL_pp_shadow}]
if {[llength $pp] != 1} { error "Expected exactly one protocol wrapper" }
report_utilization -cells $pp -file baseline_pp_utilization.rpt
report_timing -through [get_pins -of_objects $pp] -max_paths 10 -file baseline_pp_boundary_timing.rpt

set scope_root ""
set pp [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_pp_shadow || REF_NAME == KL_pp_shadow}]
if {[llength $pp] == 1} {
  set scope_root "$pp/"
} elseif {[llength $pp] == 0} {
  set core [get_cells -quiet u_pp]
  if {[llength $core] != 1 || [get_property ORIG_REF_NAME $core] ne "protocol_processor_top"} {
    error "Expected the standalone wrapper's processor instance"
  }
} else {
  error "Expected exactly one protocol wrapper"
}
set tf [open baseline_scope_timing.tsv w]
puts $tf "instance\tsequential_cells\tinternal_WNS_ns"
foreach relative {wrapper u_pp u_pp/u_aecp u_pp/u_srp u_pp/u_notify u_pp/u_listener u_pp/u_talker u_nvm} {
  set path "$scope_root$relative"
  if {$relative eq "wrapper"} {
    set path [string trimright $scope_root /]
  }
  if {$path eq ""} {
    set path KL_pp_shadow
    set regs [get_cells -hier -filter {IS_SEQUENTIAL == 1}]
  } else {
    set regs [get_cells -hier -filter [format {NAME =~ "%s/*" && IS_SEQUENTIAL == 1} $path]]
  }
  set worst [get_timing_paths -from $regs -to $regs -max_paths 1]
  if {[llength $worst] != 1} { error "No internal timing path for $path" }
  puts $tf "$path\t[llength $regs]\t[get_property SLACK $worst]"
  flush $tf
}
close $tf

write_bitstream -force alinx_ax7101.bit
quit
