# Read-only reviewer probe (R372-2) of the shipping routed checkpoint.
# Never writes a checkpoint or bitstream. Usage:
#   vivado -mode batch -nojournal -notrace -log crossings-r2.log \
#     -source vivado_probe_crossings_r2.tcl -tclargs <route.dcp> <out-dir>
# Part A: the shipping constraints as loaded. Classify each eth <-> sys/milan
#   path's exception and the LiteX attribute of its endpoint cell.
# Part B: reset_timing, recreate the two primary clocks, apply only the
#   intended 8 ns datapath-only bound in all four directions (the method the
#   round-2 record describes), and measure each direction at each model.
lassign $argv dcp out
set_param general.maxThreads 8
open_checkpoint $dcp
set rows {}

proc corner_only {c} {
    foreach x {Slow Fast} {
        config_timing_corners -corner $x -delay_type [expr {$x eq $c ? "max" : "none"}]
    }
}

proc endpoint_class {p} {
    set pin [get_property ENDPOINT_PIN $p]
    set cell [get_cells -quiet -of_objects [get_pins -quiet $pin]]
    set tags {}
    foreach a {mr_ff ars_ff1 ars_ff2} {
        if {$cell ne "" && [string toupper [get_property -quiet $a $cell]] eq "TRUE"} {lappend tags $a}
    }
    set ref [lindex [split $pin /] end]
    if {$tags eq ""} {set tags untagged}
    return "[join $tags +]:$ref"
}

set pairs {eth_clocks0_rx milansoc_crg_clkout0 milansoc_crg_clkout0 eth_clocks0_rx
           eth_clocks0_rx milansoc_crg_clkout1 milansoc_crg_clkout1 eth_clocks0_rx}

proc measure {tag} {
    upvar rows rows
    global pairs
    foreach c {Slow Fast} {
        corner_only $c
        foreach {a b} $pairs {
            set ps [get_timing_paths -from [get_clocks $a] -to [get_clocks $b] -delay_type max \
                        -max_paths 1000 -nworst 1]
            set n [llength $ps]
            if {$n == 0} {lappend rows "$tag $c $a->$b paths=0"; continue}
            set classes [dict create]
            set excs [dict create]
            set dmax 0.0
            set worst ""
            set wslack ""
            foreach p $ps {
                dict incr classes [endpoint_class $p]
                dict incr excs [get_property EXCEPTION $p]
                set d [get_property DATAPATH_DELAY $p]
                if {$d ne "" && $d > $dmax} {set dmax $d}
                set s [get_property SLACK $p]
                if {$s ne "" && ($wslack eq "" || $s < $wslack)} {set wslack $s; set worst $p}
            }
            if {$worst eq ""} {
                lappend rows [format "%s %s %s->%s paths=%d worst_slack=UNCONSTRAINED datapath_max=%.3f exceptions={%s} endpoints={%s}" \
                    $tag $c $a $b $n $dmax $excs $classes]
            } else {
                lappend rows [format "%s %s %s->%s paths=%d worst_slack=%.3f req=%s datapath_max=%.3f worst_end=%s exceptions={%s} endpoints={%s}" \
                    $tag $c $a $b $n $wslack [get_property REQUIREMENT $worst] $dmax \
                    [get_property ENDPOINT_PIN $worst] $excs $classes]
            }
        }
    }
    foreach x {Slow Fast} {config_timing_corners -corner $x -delay_type min_max}
}

# Part A: shipping constraints as loaded.
lappend rows "A clocks: [lsort [get_clocks]]"
lappend rows "A crg_clkout0 matches: [llength [get_clocks -quiet crg_clkout0]]"
lappend rows "A quasi_static cells: [llength [get_cells -hierarchical -quiet -filter {quasi_static == yes}]]"
measure A
report_clock_interaction -delay_type min_max -file $out/A_clock_interaction.rpt

# Part B: all original exceptions cleared, intended bound only.
reset_timing
create_clock -name clk200_p -period 5.0 [get_ports clk200_p]
create_clock -name eth_clocks0_rx -period 8.0 [get_ports eth_clocks0_rx]
lappend rows "B clocks after reset: [lsort [get_clocks]]"
set eth [get_clocks eth_clocks0_rx]
set sysm [get_clocks {milansoc_crg_clkout0 milansoc_crg_clkout1}]
foreach {a b} [list $eth $sysm $sysm $eth] {
    set_max_delay -datapath_only -from $a -to $b 8.000
}
measure B
report_timing -from [get_clocks milansoc_crg_clkout1] -to $eth -max_paths 20 -nworst 1 \
    -file $out/B_milan_to_eth.rpt

set f [open $out/crossings-r2-results.txt w]
foreach r $rows {puts $f $r; puts $r}
close $f
exit
