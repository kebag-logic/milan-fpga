head a2690e682d929e6d3811006f961a24361827c596
command: tools/prep_directives3.py
full log: 7290 bytes, sha256 7603a278b92eb108ad2de05017177c9555eabd6ab4888be6fa70c4d7ef1f10c9
---
set_param general.maxThreads 32
open_checkpoint {<scratch>/route/split/gateware/alinx_ax7101_synth.dcp}
# Add pre-optimize commands

source {<scratch>/route/src/sw/litex/clock_constraints.tcl}
kl_quasi_static_constraints
milan_eth_constraints eth_clocks0_rx [list milansoc_crg_clkout0 milansoc_crg_clkout1] [list milansoc_crg_pll_audio_fb milansoc_crg_audio_ref_raw milansoc_crg_audio_mclk_raw milansoc_crg_clkout2]
kl_servo_reset_sync_constraints milansoc_crg_clkout1

# Optimize design

opt_design -directive ExploreArea

# Add pre-placement commands

source {<scratch>/route/src/sw/litex/timing_grade.tcl}
kl_timing_grade_configure {xc7a100t-fgg484-2} {commercial} {0} {85} {Slow Fast}

# Placement

place_design -directive ExtraTimingOpt
phys_opt_design -directive AggressiveExplore

# Placement report

report_utilization -hierarchical -file alinx_ax7101_utilization_hierarchical_place.rpt
report_utilization -file alinx_ax7101_utilization_place.rpt
report_io -file alinx_ax7101_io.rpt
report_control_sets -verbose -file alinx_ax7101_control_sets.rpt
report_clock_utilization -file alinx_ax7101_clock_utilization.rpt
write_checkpoint -force alinx_ax7101_place.dcp

# Add pre-routing commands

source {<scratch>/route/src/sw/litex/iob_pack_check.tcl}
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

set baseline_placement {full-split}
set placement_file [open baseline_placement.tsv w]
puts $placement_file "placement	role	count"
set placement_cells [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_pp_shadow || REF_NAME == KL_pp_shadow}]
set placement_count [llength $placement_cells]
if {$placement_count < 0 || $placement_count > 0} {
  error "wrong placement full-split: wrapper (KL_pp_shadow) count $placement_count, expected 0..0"
}
puts $placement_file "full-split	wrapper	$placement_count"
set placement_cells [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_adp_engine || REF_NAME == KL_adp_engine}]
set placement_count [llength $placement_cells]
if {$placement_count < 0 || $placement_count > 0} {
  error "wrong placement full-split: adp (KL_adp_engine) count $placement_count, expected 0..0"
}
puts $placement_file "full-split	adp	$placement_count"
set placement_cells [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_pp_acmp_listener || REF_NAME == KL_pp_acmp_listener}]
set placement_count [llength $placement_cells]
if {$placement_count < 0 || $placement_count > 0} {
  error "wrong placement full-split: acmp-listener (KL_pp_acmp_listener) count $placement_count, expected 0..0"
}
puts $placement_file "full-split	acmp-listener	$placement_count"
set placement_cells [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_acmp_talker || REF_NAME == KL_acmp_talker}]
set placement_count [llength $placement_cells]
if {$placement_count < 0 || $placement_count > 0} {
  error "wrong placement full-split: acmp-talker (KL_acmp_talker) count $placement_count, expected 0..0"
}
puts $placement_file "full-split	acmp-talker	$placement_count"
set placement_cells [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_srp_top || REF_NAME == KL_srp_top}]
set placement_count [llength $placement_cells]
if {$placement_count < 0 || $placement_count > 0} {
  error "wrong placement full-split: srp (KL_srp_top) count $placement_count, expected 0..0"
}
puts $placement_file "full-split	srp	$placement_count"
set placement_cells [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_maap || REF_NAME == KL_maap}]
set placement_count [llength $placement_cells]
if {$placement_count < 0 || $placement_count > 0} {
  error "wrong placement full-split: maap (KL_maap) count $placement_count, expected 0..0"
}
puts $placement_file "full-split	maap	$placement_count"
set placement_cells [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_pp_maap || REF_NAME == KL_pp_maap}]
set placement_count [llength $placement_cells]
if {$placement_count < 0 || $placement_count > 0} {
  error "wrong placement full-split: processor-maap (KL_pp_maap) count $placement_count, expected 0..0"
}
puts $placement_file "full-split	processor-maap	$placement_count"
set placement_cells [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_aecp_engine || REF_NAME == KL_aecp_engine}]
set placement_count [llength $placement_cells]
if {$placement_count < 0 || $placement_count > 0} {
  error "wrong placement full-split: aecp (KL_aecp_engine) count $placement_count, expected 0..0"
}
puts $placement_file "full-split	aecp	$placement_count"
set placement_cells [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_aecp_notify || REF_NAME == KL_aecp_notify}]
set placement_count [llength $placement_cells]
if {$placement_count < 0 || $placement_count > 0} {
  error "wrong placement full-split: notify (KL_aecp_notify) count $placement_count, expected 0..0"
}
puts $placement_file "full-split	notify	$placement_count"
set placement_cells [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_mbx || REF_NAME == KL_mbx}]
set placement_count [llength $placement_cells]
if {$placement_count < 1 || $placement_count > 1} {
  error "wrong placement full-split: mailbox (KL_mbx) count $placement_count, expected 1..1"
}
puts $placement_file "full-split	mailbox	$placement_count"
set placement_cells [get_cells -quiet -hier -filter {ORIG_REF_NAME == KL_gptp_shadow || REF_NAME == KL_gptp_shadow}]
set placement_count [llength $placement_cells]
if {$placement_count < 1 || $placement_count > 1} {
  error "wrong placement full-split: gptp (KL_gptp_shadow) count $placement_count, expected 1..1"
}
puts $placement_file "full-split	gptp	$placement_count"
close $placement_file

report_utilization -hierarchical -hierarchical_depth 10 -hierarchical_min_primitive_count 0 -file baseline_hierarchy.rpt
report_utilization -file baseline_utilization.rpt
report_timing_summary -max_paths 10 -file baseline_timing.rpt
set pf [open baseline_cells.tsv w]
puts $pf "cell\tprimitive"
foreach c [get_cells -hier -filter {IS_PRIMITIVE == 1}] {
  puts $pf "$c\t[get_property REF_NAME $c]"
}
close $pf

set regs [get_cells -hier -filter {IS_SEQUENTIAL == 1}]
set worst [get_timing_paths -from $regs -to $regs -max_paths 1]
if {[llength $worst] != 1} { error "No internal timing path for selected image" }
set tf [open baseline_scope_timing.tsv w]
puts $tf "instance\tsequential_cells\tinternal_WNS_ns"
puts $tf "image\t[llength $regs]\t[get_property SLACK $worst]"
close $tf

quit
