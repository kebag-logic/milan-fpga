# Read-only reviewer probe (R372-3) of the shipping routed checkpoint.
# Never writes a checkpoint or bitstream. Usage:
#   vivado -mode batch -nojournal -notrace -log s1.log \
#     -source probe_s1_reset_endpoints.tcl -tclargs <route.dcp> <out-file>
# Under the shipping constraints as loaded, list every timing path from the
# sys and milan clocks into the Ethernet clock's ars_ff1/ars_ff2 PRE pins and
# mr_ff D pins, with the exception that governs it (per path for PRE pins).
lassign $argv dcp outf
set_param general.maxThreads 8
open_checkpoint $dcp
set rows {}
set eth [get_clocks eth_clocks0_rx]
set ars_pre [get_pins -filter {REF_PIN_NAME == PRE} -of_objects \
    [get_cells -hierarchical -filter {ars_ff1 == TRUE || ars_ff2 == TRUE}]]
set mr_d [get_pins -filter {REF_PIN_NAME == D} -of_objects \
    [get_cells -hierarchical -filter {mr_ff == TRUE}]]
lappend rows "all ars PRE pins: [llength $ars_pre]; all mr_ff D pins: [llength $mr_d]"
foreach src {milansoc_crg_clkout0 milansoc_crg_clkout1} {
    foreach {tag pins} [list arsPRE $ars_pre mrD $mr_d] {
        foreach c {Slow Fast} {
            foreach x {Slow Fast} {
                config_timing_corners -corner $x -delay_type [expr {$x eq $c ? "max" : "none"}]
            }
            set ps [get_timing_paths -from [get_clocks $src] -to $pins -delay_type max \
                        -max_paths 1000 -nworst 1]
            set ex [dict create]
            set capt [dict create]
            set ends {}
            foreach p $ps {
                dict incr ex [get_property EXCEPTION $p]
                dict incr capt [get_property ENDPOINT_CLOCK $p]
                lappend ends [get_property ENDPOINT_PIN $p]
                if {$tag eq "arsPRE"} {
                    lappend rows [format "  %s %s path %s -> %s capture=%s exception={%s} slack=%s" $c $src \
                        [get_property STARTPOINT_PIN $p] [get_property ENDPOINT_PIN $p] \
                        [get_property ENDPOINT_CLOCK $p] [get_property EXCEPTION $p] [get_property SLACK $p]]
                }
            }
            lappend rows [format "%s %s->%s paths=%d capture={%s} exceptions={%s} endpoints={%s}" \
                $c $src $tag [llength $ps] $capt $ex [lsort $ends]]
        }
    }
}
foreach x {Slow Fast} {config_timing_corners -corner $x -delay_type min_max}
set f [open $outf w]
foreach r $rows {puts $f $r; puts $r}
close $f
exit
