# Independent structural classification of the Ethernet crossings in the
# shipping routed checkpoint, under the shipping constraints as loaded.
# Usage: vivado -mode batch -source classify_crossings.tcl -tclargs <route.dcp> <out.txt>
# Read-only: opens a copy of the checkpoint, writes nothing back.
set dcp [lindex $argv 0]
set out [open [lindex $argv 1] w]
set_param general.maxThreads 8
open_checkpoint $dcp

set eth [get_clocks -of_objects [get_ports eth_clocks0_rx]]
set sys [get_clocks milansoc_crg_clkout0]
set mil [get_clocks milansoc_crg_clkout1]
puts $out "eth=$eth sys=$sys milan=$mil"
puts $out "crg_clkout0 matches: [llength [get_clocks -quiet crg_clkout0]]"

proc clk_of_pin {p} { return [lsort -unique [get_clocks -quiet -of_objects $p]] }
proc launch_clks {p} {
    set sps [all_fanin -quiet -flat -startpoints_only $p]
    set cl {}
    foreach sp $sps { foreach c [get_clocks -quiet -of_objects $sp] { lappend cl $c } }
    return [lsort -unique $cl]
}

# Class 1: MultiReg (mr_ff) D endpoints; class 2: AsyncResetSynchronizer PRE.
array set cnt {}
foreach cell [get_cells -hierarchical -filter {mr_ff == TRUE}] {
    set d [get_pins -of_objects $cell -filter {REF_PIN_NAME == D}]
    set cap [clk_of_pin [get_pins -of_objects $cell -filter {REF_PIN_NAME == C}]]
    foreach l [launch_clks $d] { foreach c $cap {
        if {$l ne $c} { incr cnt(mr_ff:D,$l,$c) }
    } }
}
foreach cell [get_cells -hierarchical -filter {ars_ff1 == TRUE || ars_ff2 == TRUE}] {
    set p [get_pins -of_objects $cell -filter {REF_PIN_NAME == PRE}]
    if {[llength $p] == 0} { continue }
    set cap [clk_of_pin [get_pins -of_objects $cell -filter {REF_PIN_NAME == C}]]
    foreach l [launch_clks $p] { foreach c $cap {
        if {$l ne $c} { incr cnt(ars:PRE,$l,$c); lappend who(ars:PRE,$l,$c) $cell }
    } }
}
foreach k [lsort [array names cnt]] {
    set parts [split $k ,]
    set l [lindex $parts 1]; set c [lindex $parts 2]
    if {$l eq $eth || $c eq $eth} {
        puts $out "STRUCT $k count=$cnt($k)"
        if {[info exists who($k)]} { puts $out "  cells: [lsort $who($k)]" }
    }
}

# Timed/untimed endpoints per direction under the shipping constraints.
foreach {name from to} [list eth_to_sys $eth $sys sys_to_eth $sys $eth eth_to_milan $eth $mil milan_to_eth $mil $eth] {
    foreach corner {Slow Fast} {
        config_timing_corners -corner $corner -delay_type min_max
        foreach other {Slow Fast} { if {$other ne $corner} { config_timing_corners -corner $other -delay_type none } }
        set paths [get_timing_paths -quiet -from $from -to $to -max_paths 5000 -nworst 1 -setup]
        array unset ep
        set worst ""
        foreach p $paths {
            set e [get_property ENDPOINT_PIN $p]
            set cell [get_cells -of_objects $e]
            set pin [get_property REF_PIN_NAME $e]
            set tag untagged
            if {[string is true -strict [get_property -quiet mr_ff $cell]]} { set tag mr_ff }
            if {[string is true -strict [get_property -quiet ars_ff1 $cell]] || [string is true -strict [get_property -quiet ars_ff2 $cell]]} { set tag ars }
            set ex [get_property EXCEPTION $p]
            if {$ex eq ""} { set ex timed }
            incr ep($tag:$pin|$ex)
        }
        puts $out "PATHS $corner $name n=[llength $paths] classes=[array get ep]"
    }
}
close $out
