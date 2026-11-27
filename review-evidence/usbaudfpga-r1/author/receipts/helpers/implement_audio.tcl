# Reproduce the accepted route from its current-source synthesis checkpoint.
# Arguments: checkpoint optimization placement clock_rules boundary_timing fifo_rules bridge_crossings corner_rules audio_pad_rules board_pad_rules
set_param general.maxThreads 2
set checkpoint [lindex $argv 0]
set opt_directive [lindex $argv 1]
set place_directive [lindex $argv 2]
open_checkpoint $checkpoint
# Add pre-optimize commands

source [lindex $argv 3]
kl_quasi_static_constraints
kl_servo_reset_sync_constraints milansoc_clkout2
read_xdc [lindex $argv 4]
source [lindex $argv 5]
source [lindex $argv 6]
source [lindex $argv 7]
kl_timing_grade_configure xc7a100tcsg324-1 commercial 0 85 {Slow Fast}

# Optimize design

opt_design -directive $opt_directive

# Add pre-placement commands


# Placement

place_design -directive $place_directive
phys_opt_design -directive AggressiveExplore

# Placement report

report_utilization -hierarchical -file digilent_arty_utilization_hierarchical_place.rpt
report_utilization -file digilent_arty_utilization_place.rpt
report_io -file digilent_arty_io.rpt
report_control_sets -verbose -file digilent_arty_control_sets.rpt
report_clock_utilization -file digilent_arty_clock_utilization.rpt
write_checkpoint -force digilent_arty_place.dcp

# Add pre-routing commands

source [lindex $argv 8]
kl_audio_pack_check digilent_arty_audio_packing.rpt
source [lindex $argv 9]
kl_iob_pack_check digilent_arty_iob_pack.rpt

# Routing

route_design -directive AggressiveExplore
phys_opt_design -directive AggressiveExplore
write_checkpoint -force digilent_arty_route.dcp

# Routing report

report_timing_summary -no_header -no_detailed_paths
report_route_status -file digilent_arty_route_status.rpt
report_drc -file digilent_arty_drc.rpt
report_timing_summary -datasheet -max_paths 10 -file digilent_arty_timing.rpt
report_power -file digilent_arty_power.rpt
set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]
set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 1 [current_design]
set_property BITSTREAM.CONFIG.CONFIGRATE 33 [current_design]

# Bitstream generation

write_bitstream -force digilent_arty.bit 
write_cfgmem -force -format bin -interface spix1 -size 16 -loadbit "up 0x0 digilent_arty.bit" -file digilent_arty.bin
kl_timing_grade_reports digilent_arty_audio
report_bus_skew -file digilent_arty_audio_bus_skew.rpt
report_utilization -file digilent_arty_audio_utilization_route.rpt
report_timing -from [get_cells usb_gpif/flag_meta_r_reg] -to [get_cells usb_gpif/flag_sync_r_reg] -delay_type min_max -max_paths 2 -file digilent_arty_audio_flag_sync.rpt

# End

quit