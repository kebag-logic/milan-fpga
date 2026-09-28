# Read-only per-corner reports for #607; all paths are supplied as arguments.
set_param general.maxThreads 16
set checkpoint [lindex $argv 0]
set prefix [lindex $argv 1]
open_checkpoint $checkpoint
set eth [get_clocks -of_objects [get_ports eth_clocks0_rx]]
set sys [get_clocks -of_objects [get_nets sys_clk]]
set milan [get_clocks -of_objects [get_nets milan_clk]]
foreach clock [list $eth $sys $milan] {
    if {[llength $clock] != 1} {error "expected one crossing clock: $clock"}
}
set_operating_conditions -grade commercial -junction_temp 85
set table [open ${prefix}_crossings.tsv w]
puts $table "temperature_C\tcorner\tfrom\tto\tslack_ns\trequirement_ns\tdatapath_ns\tstartpoint\tendpoint"
foreach temperature {0 85} {
    set_operating_conditions -junction_temp $temperature
    foreach corner {Slow Fast} {
        foreach candidate {Slow Fast} {
            if {$candidate eq $corner} {
                config_timing_corners -corner $candidate -delay_type min_max
            } else {
                config_timing_corners -corner $candidate -delay_type none
            }
        }
        set stem ${prefix}_${corner}_${temperature}C
        report_timing_summary -delay_type min_max -report_unconstrained -check_timing_verbose \
            -max_paths 5 -file ${stem}_timing.rpt
        report_clock_interaction -delay_type min_max -file ${stem}_interaction.rpt
        foreach {label from to} [list eth_sys $eth $sys sys_eth $sys $eth \
                                    eth_milan $eth $milan milan_eth $milan $eth] {
            set paths [get_timing_paths -from $from -to $to -delay_type max -max_paths 1]
            if {[llength $paths] != 1} {error "no bounded data path for $label"}
            set path [lindex $paths 0]
            set slack [get_property SLACK $path]
            set requirement [get_property REQUIREMENT $path]
            set delay [get_property DATAPATH_DELAY $path]
            puts $table "$temperature\t$corner\t$from\t$to\t$slack\t$requirement\t$delay\t[get_property STARTPOINT_PIN $path]\t[get_property ENDPOINT_PIN $path]"
            if {$requirement != 8.0} {error "wrong Ethernet requirement $requirement for $label"}
            report_timing -from $from -to $to -delay_type max -max_paths 100 \
                -file ${stem}_${label}.rpt
        }
    }
}
close $table
foreach corner {Slow Fast} {config_timing_corners -corner $corner -delay_type min_max}
report_clock_interaction -delay_type min_max -file ${prefix}_interaction.rpt
report_exceptions -file ${prefix}_exceptions.rpt
report_timing_summary -delay_type min_max -report_unconstrained -file ${prefix}_combined_timing.rpt
quit
