# #817: read-only. The worst setup slack of the families that set WNS at dev and at the head, in one routed
# checkpoint; then, as a diagnostic only, the two clocks declared asynchronous in memory, so report_cdc
# classifies the servo synchronizer's structure (a related-clock point exception is never analysed
# structurally). Nothing is written back.
# usage: vivado -mode batch -source cross_probe.tcl -tclargs <routed.dcp> <outdir>
lassign $argv dcp out
set_param general.maxThreads 8
file mkdir $out
open_checkpoint $dcp
set fh [open $out/families.tsv w]
puts $fh "family\tworst_setup_slack\tlevels\tstartpoint\tendpoint"
foreach {name kind pattern} {
    zqcs_timer_to_bank_machines from {milansoc_sdram_zqcs_timer_count1_reg*}
    eth_tx_crc_to_gptp_launch to {KL_gptp_gmii_launch/mine_r_reg}
    milan_to_ps_handshake to {*mmcm_servo/u_batch_hs/*}
} {
    set cells [get_cells -quiet -hierarchical -filter "NAME =~ \"$pattern\" && IS_SEQUENTIAL"]
    if {![llength $cells]} {set cells [get_cells -quiet $pattern]}
    if {$kind eq "from"} {
        set p [get_timing_paths -quiet -from $cells -delay_type max -max_paths 1]
    } else {
        set p [get_timing_paths -quiet -to $cells -delay_type max -max_paths 1]
    }
    puts $fh "$name\t[get_property -quiet SLACK $p]\t[get_property -quiet LOGIC_LEVELS $p]\t[get_property -quiet STARTPOINT_PIN $p]\t[get_property -quiet ENDPOINT_PIN $p]"
}
close $fh
set first [get_cells -hierarchical -filter {NAME =~ "*mmcm_servo/psrst_sync_r_reg[0]"}]
set ps [get_clocks -of_objects [get_pins -of_objects $first -filter {IS_CLOCK == 1}]]
set milan [get_clocks -of_objects [get_nets milansoc_crg_clkout1]]
set_clock_groups -asynchronous -group $milan -group $ps
report_cdc -from $milan -to $ps -summary -file $out/diag_async_cdc_summary.rpt
report_cdc -from $milan -to $ps -details -file $out/diag_async_cdc_details.rpt
puts "CROSS-PROBE-DONE"
