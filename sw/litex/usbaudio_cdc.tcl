# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Apply after synthesis, when the actual crossing endpoints exist.
set usb_gray_source [get_cells -hier -regexp {usb_audio_bridge/clock_stamp/gray_r_reg\[[0-9]+\]}]
set usb_gray_meta [get_cells -hier -regexp {usb_audio_bridge/clock_stamp/meta_r_reg\[[0-9]+\]}]
if {[llength $usb_gray_source] != 48 || [llength $usb_gray_meta] != 48} {
    error "Audio timestamp crossing must retain all 48 Gray bits"
}
set_max_delay -datapath_only 20.000 -from $usb_gray_source -to $usb_gray_meta
set_bus_skew 20.000 -from $usb_gray_source -to $usb_gray_meta
# Only the first synchronizer stages are asynchronous endpoints.
set usb_levels [get_cells -hier -regexp {usb_audio_bridge/(lock_r|error_r)_reg\[0\]}]
set_false_path -to [get_pins -of_objects $usb_levels -filter {REF_PIN_NAME == D}]
set usb_running [get_cells -hier -regexp {usb_audio_bridge/running_meta_r_reg\[[01]\]}]
set_false_path -to [get_pins -of_objects $usb_running -filter {REF_PIN_NAME == D}]
# Assertion is asynchronous; local two-edge release remains timed.
set usb_reset_cells [get_cells -hier -filter {ORIG_REF_NAME == KL_usbaudio_reset || REF_NAME == KL_usbaudio_reset}]
foreach inst $usb_reset_cells {
    set_false_path -to [get_pins -hier -regexp [format {%s/release_r_reg\[[01]\]/CLR} $inst]]
}
