# Reviewer probe: Slow-corner datapath of the false-pathed eth-RX <-> sys crossings
# (LiteEth MAC gray pointers and pulse synchronizers) on a COPY of the routed checkpoint.
#   vivado -mode batch -nojournal -notrace -log skew.log -source falsepath_skew_probe.tcl -tclargs <route.dcp copy>
set_param general.maxThreads 8
lassign $argv dcp
open_checkpoint $dcp
config_timing_corners -corner Fast -delay_type none
config_timing_corners -corner Slow -delay_type min_max
set eth [get_clocks eth_clocks0_rx]
set sys [get_clocks milansoc_crg_clkout0]
foreach {label from to} [list eth-to-sys $eth $sys sys-to-eth $sys $eth] {
    set paths [get_timing_paths -from $from -to $to -delay_type max -max_paths 1000 -nworst 1]
    set worst 0.0; set wp ""
    foreach p $paths {
        set d [get_property DATAPATH_DELAY $p]
        if {$d > $worst} {set worst $d; set wp "[get_property STARTPOINT_PIN $p] -> [get_property ENDPOINT_PIN $p]"}
    }
    puts [format "SKEW %s endpoints=%d exception=<%s> max_datapath_ns=%.3f worst=%s" \
        $label [llength $paths] [get_property EXCEPTION [lindex $paths 0]] $worst $wp]
}
puts "SKEW FINISHED"
exit
