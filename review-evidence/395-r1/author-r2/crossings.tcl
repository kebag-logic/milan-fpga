# Read-only reviewer probe: measure the eth <-> sys/milan crossing data-path
# delays that the shipping constraints leave false-pathed, by clearing the
# in-memory constraints and re-applying only the two primary clocks plus the
# 8 ns datapath-only bound that sw/litex/milan_soc.py:1499-1534 intends.
# Never writes a checkpoint or bitstream. Usage:
#   vivado -mode batch -nojournal -notrace -log crossings.log \
#     -source vivado_probe_crossings.tcl -tclargs <route.dcp> <out-dir>
lassign $argv dcp out
set_param general.maxThreads 8
open_checkpoint $dcp
reset_timing
create_clock -name clk200_p -period 5.0 [get_ports clk200_p]
create_clock -name eth_clocks0_rx -period 8.0 [get_ports eth_clocks0_rx]
set rows [list "clocks after reset: [lsort [get_clocks]]"]
set eth [get_clocks eth_clocks0_rx]
set sysm [get_clocks {milansoc_crg_clkout0 milansoc_crg_clkout1}]
foreach {a b} [list $eth $sysm $sysm $eth] {
    set_max_delay -datapath_only -from $a -to $b 8.000
}
foreach c {Slow Fast} {
    foreach x {Slow Fast} {
        config_timing_corners -corner $x -delay_type [expr {$x eq $c ? "max" : "none"}]
    }
    foreach {a b} {eth_clocks0_rx milansoc_crg_clkout0 milansoc_crg_clkout0 eth_clocks0_rx eth_clocks0_rx milansoc_crg_clkout1 milansoc_crg_clkout1 eth_clocks0_rx} {
        set ps [get_timing_paths -from [get_clocks $a] -to [get_clocks $b] -delay_type max \
                    -max_paths 200 -nworst 1]
        set dmax 0.0
        foreach p $ps {
            set d [get_property DATAPATH_DELAY $p]
            if {$d ne "" && $d > $dmax} {set dmax $d}
        }
        set w [lindex $ps 0]
        lappend rows [format "%s %s->%s paths=%d worst_slack=%s req=%s datapath_max=%.3f worst_end=%s" \
            $c $a $b [llength $ps] [get_property SLACK $w] [get_property REQUIREMENT $w] $dmax \
            [get_property ENDPOINT_PIN $w]]
    }
}
foreach x {Slow Fast} {config_timing_corners -corner $x -delay_type min_max}
report_timing -from $eth -to [get_clocks milansoc_crg_clkout0] -max_paths 20 -nworst 1 \
    -file $out/eth_to_sys_bounded.rpt
set f [open $out/crossings-results.txt w]
foreach r $rows {puts $f $r; puts $r}
close $f
exit
