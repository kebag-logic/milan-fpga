# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Public A1:A0 harness budget, USB-audio #9, 50 MHz, 200-ohm controls.
create_generated_clock -name usb_gpif_pin -source [get_pins usb_pclk_forward/C] -divide_by 1 [get_ports usbaudio_pclk]
set usb_capture_clock [get_clocks -of_objects [get_pins usb_mmcm/CLKOUT2]]
set_input_delay -clock usb_gpif_pin -max 12.890 [get_ports {usbaudio_dq[*]}]
set_input_delay -clock usb_gpif_pin -min 2.250 [get_ports {usbaudio_dq[*]}]
set_multicycle_path -setup 2 -from [get_clocks usb_gpif_pin] -to $usb_capture_clock
set_input_delay -clock usb_gpif_pin -max 16.870 [get_ports usbaudio_flaga]
set_input_delay -clock usb_gpif_pin -min 0.410 [get_ports usbaudio_flaga]
set_max_delay -datapath_only -from [get_ports usbaudio_flaga] -to [get_cells usb_gpif/flag_meta_r_reg] 21.870
set_max_delay -datapath_only -from [get_cells usb_gpif/flag_meta_r_reg] -to [get_cells usb_gpif/flag_sync_r_reg] 2.000
set_output_delay -clock usb_gpif_pin -max 4.050 [get_ports {usbaudio_dq[*]}]
set_output_delay -clock usb_gpif_pin -min -5.610 [get_ports {usbaudio_dq[*]}]
set usb_controls [get_ports {usbaudio_addr[*] usbaudio_slwr_n usbaudio_slrd_n usbaudio_sloe_n usbaudio_pktend_n}]
set_output_delay -clock usb_gpif_pin -max 8.710 $usb_controls
set_output_delay -clock usb_gpif_pin -min -5.390 $usb_controls
set_clock_uncertainty 0.200 [get_clocks usb_gpif_pin]
set_clock_uncertainty 0.200 -from [get_clocks usb_gpif_pin] -to $usb_capture_clock
set_property DRIVE 8 [get_ports {usbaudio_dq[*] usbaudio_addr[*] usbaudio_pclk usbaudio_slwr_n usbaudio_slrd_n usbaudio_sloe_n usbaudio_pktend_n}]
set_property SLEW FAST [get_ports {usbaudio_dq[*] usbaudio_addr[*] usbaudio_pclk usbaudio_slwr_n usbaudio_slrd_n usbaudio_sloe_n usbaudio_pktend_n}]
