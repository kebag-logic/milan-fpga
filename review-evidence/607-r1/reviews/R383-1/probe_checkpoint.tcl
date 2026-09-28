# [R383] read-only probe of a routed #607 sweep checkpoint (never writes a checkpoint).
# Usage: vivado -mode batch -source probe_checkpoint.tcl -tclargs <route.dcp> <out_prefix> <repo_hook_tcl>
set_param general.maxThreads 8
lassign $argv checkpoint prefix hook
open_checkpoint $checkpoint
set out [open ${prefix}_summary.txt w]
proc say {msg} { global out; puts $out $msg; puts "PROBE: $msg" }

set eth [get_clocks -of_objects [get_ports eth_clocks0_rx]]
set sys [get_clocks -of_objects [get_nets sys_clk]]
set milan [get_clocks -of_objects [get_nets milan_clk]]
say "clocks eth=$eth sys=$sys milan=$milan all=[lsort [get_clocks]]"

# 1. Full-precision worst setup/hold per speed model, both models analysed in turn.
foreach corner {Slow Fast} {
    foreach c {Slow Fast} {
        config_timing_corners -corner $c -delay_type [expr {$c eq $corner ? "min_max" : "none"}]
    }
    update_timing -full
    set s [lindex [get_timing_paths -delay_type max -max_paths 1] 0]
    set h [lindex [get_timing_paths -delay_type min -max_paths 1] 0]
    say "corner=$corner WNS=[get_property SLACK $s] from=[get_property STARTPOINT_PIN $s] to=[get_property ENDPOINT_PIN $s] req=[get_property REQUIREMENT $s]"
    say "corner=$corner WHS=[get_property SLACK $h]"
    report_timing -delay_type max -max_paths 1 -significant_digits 6 -file ${prefix}_${corner}_wns_6digit.rpt
}
foreach c {Slow Fast} {config_timing_corners -corner $c -delay_type min_max}
update_timing -full

# 2. Every Ethernet crossing endpoint and its exception, from the CDC engine.
report_cdc -from $eth -to [list $sys $milan] -details -file ${prefix}_cdc_eth_to_part.rpt
report_cdc -from [list $sys $milan] -to $eth -details -file ${prefix}_cdc_part_to_eth.rpt
report_cdc -details -file ${prefix}_cdc_all.rpt
report_clock_interaction -delay_type min_max -file ${prefix}_interaction.rpt
report_exceptions -from $eth -to [list $sys $milan] -file ${prefix}_exc_eth_to_part.rpt
report_exceptions -from [list $sys $milan] -to $eth -file ${prefix}_exc_part_to_eth.rpt
check_timing -verbose -file ${prefix}_check_timing.rpt

# 3. Count bounded max-delay endpoints per direction.
proc bounded {from to} {
    set paths [get_timing_paths -from $from -to $to -delay_type max -max_paths 100000 -nworst 1 -unique_pins]
    set n [llength $paths]; set bad 0; set worst 1e9
    foreach p $paths {
        if {[get_property REQUIREMENT $p] != 8.0} {incr bad}
        set sl [get_property SLACK $p]
        if {$sl < $worst} {set worst $sl}
    }
    return "paths=$n non8req=$bad worst=$worst"
}
foreach {label from to} [list eth_sys $eth $sys sys_eth $sys $eth eth_milan $eth $milan milan_eth $milan $eth] {
    say "bound $label [bounded $from $to]"
}

# 4. Mutation (in memory only): re-apply LiteX's unscoped MultiReg false path.
#    If the scoping matters, bounded endpoints into MultiReg first stages disappear.
set_false_path -quiet -to [get_cells -hierarchical -filter {mr_ff == TRUE}]
update_timing -full
foreach {label from to} [list eth_sys $eth $sys sys_eth $sys $eth eth_milan $eth $milan milan_eth $milan $eth] {
    say "after_generic_mask bound $label [bounded $from $to]"
}
report_clock_interaction -delay_type min_max -file ${prefix}_interaction_after_generic_mask.rpt

# 5. Wrong-name refusal of the committed hook (in memory; the design is not saved).
source $hook
foreach {label cmd} {
    wrong_port {milan_eth_constraints eth_clocks9_rx [list milansoc_crg_clkout0] [list]}
    wrong_net  {milan_eth_constraints eth_clocks0_rx [list crg_clkout0] [list]}
    wrong_other {milan_eth_constraints eth_clocks0_rx [list milansoc_crg_clkout0] [list crg_clkout4]}
} {
    set rc [catch $cmd msg]
    say "hook $label rc=$rc msg=[string range $msg 0 200]"
}
close $out
quit
