# Reviewer probe (R373-2): Ethernet <-> sys/milan crossings on a COPY of the
# shipping routed checkpoint, measured per timing model in three constraint
# states. Writes only report files into the current directory; never writes a
# checkpoint or bitstream.
#   vivado -mode batch -nojournal -notrace -log crossing.log \
#     -source crossing_probe_r2.tcl -tclargs <route.dcp copy>
# A: as shipped.  B: the source's intended exceptions (sw/litex/milan_soc.py
# :1520-1534) added in memory with the real clock names, everything else kept.
# C: reset_timing, primaries recreated from the shipping XDC (:557, :559), and
# only the 8 ns datapath-only bound applied in all four directions, so every
# crossing hidden by any false path is exposed.
set_param general.maxThreads 8
lassign $argv dcp
open_checkpoint $dcp
puts "R2 part=[get_property PART [current_design]]"
puts "R2 quasi_static cells=[llength [get_cells -hierarchical -quiet -filter {quasi_static == "yes"}]]"
foreach name {crg_clkout0 crg_clkout1 crg_audio_ref_raw} {
    puts "R2 get_clocks $name -> '[get_clocks -quiet $name]'"
}
set pairs {eth_clocks0_rx milansoc_crg_clkout0 milansoc_crg_clkout0 eth_clocks0_rx
           eth_clocks0_rx milansoc_crg_clkout1 milansoc_crg_clkout1 eth_clocks0_rx}

proc measure {tag pairs} {
    foreach corner {Slow Fast} {
        foreach x {Slow Fast} {
            config_timing_corners -corner $x -delay_type [expr {$x eq $corner ? "min_max" : "none"}]
        }
        foreach {a b} $pairs {
            foreach type {max min} {
                set ps [get_timing_paths -from [get_clocks $a] -to [get_clocks $b] -delay_type $type \
                            -max_paths 1000 -nworst 1]
                set timed 0; set fp 0; set worst ""; set wp ""; set dmax 0.0; set ends {}
                foreach p $ps {
                    set s [get_property SLACK $p]
                    lappend ends [get_property ENDPOINT_PIN $p]
                    if {$s eq ""} {incr fp; continue}
                    incr timed
                    set d [get_property DATAPATH_DELAY $p]
                    if {$d > $dmax} {set dmax $d}
                    if {$worst eq "" || $s < $worst} {set worst $s; set wp $p}
                }
                set req [expr {$wp eq "" ? "-" : [get_property REQUIREMENT $wp]}]
                set exc [expr {$wp eq "" ? "-" : [get_property EXCEPTION $wp]}]
                set end [expr {$wp eq "" ? "-" : [get_property ENDPOINT_PIN $wp]}]
                puts [format "R2 %s %s %s %s->%s endpoints=%d timed=%d falsepath=%d worst_slack=%s req=%s exception=<%s> datapath_max=%.3f worst_end=%s" \
                      $tag $corner $type $a $b [llength [lsort -unique $ends]] $timed $fp $worst $req $exc $dmax $end]
            }
        }
    }
    foreach x {Slow Fast} {config_timing_corners -corner $x -delay_type min_max}
}

measure A_shipped $pairs
report_clock_interaction -delay_type min_max -file r2_clock_interaction_shipped.rpt

set eth [get_clocks eth_clocks0_rx]
set part_cks [get_clocks {milansoc_crg_clkout0 milansoc_crg_clkout1}]
foreach {a b} [list $eth $part_cks $part_cks $eth] {
    set_false_path -hold -from $a -to $b
    set_max_delay -datapath_only -from $a -to $b 8.000
}
measure B_intended_names $pairs
report_clock_interaction -delay_type min_max -file r2_clock_interaction_intended.rpt

reset_timing
create_clock -name clk200_p -period 5.0 [get_ports clk200_p]
create_clock -name eth_clocks0_rx -period 8.0 [get_ports eth_clocks0_rx]
puts "R2 clocks after reset: [lsort [get_clocks]]"
set eth [get_clocks eth_clocks0_rx]
set part_cks [get_clocks {milansoc_crg_clkout0 milansoc_crg_clkout1}]
foreach {a b} [list $eth $part_cks $part_cks $eth] {
    set_max_delay -datapath_only -from $a -to $b 8.000
}
measure C_all_exposed $pairs
# Every exposed milan->Ethernet endpoint, Slow model, to classify reset vs data.
config_timing_corners -corner Fast -delay_type none
foreach p [get_timing_paths -from [get_clocks milansoc_crg_clkout1] -to $eth -delay_type max \
               -max_paths 1000 -nworst 1] {
    puts [format "R2 C_endpoint Slow clkout1->eth slack=%s datapath=%.3f from=%s to=%s" \
          [get_property SLACK $p] [get_property DATAPATH_DELAY $p] \
          [get_property STARTPOINT_PIN $p] [get_property ENDPOINT_PIN $p]]
}
config_timing_corners -corner Fast -delay_type min_max
puts "R2 FINISHED"
exit
