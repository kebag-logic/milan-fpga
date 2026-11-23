set_param general.maxThreads 16
open_checkpoint ../measure_opt.dcp


source {$CHECKOUT/sw/litex/timing_grade.tcl}
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

source {$CHECKOUT/sw/litex/iob_pack_check.tcl}
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


report_utilization -hierarchical -file routed_hier.rpt
report_utilization -file routed_util.rpt
quit
