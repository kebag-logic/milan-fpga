# Read-only reviewer probe of the shipping routed checkpoint. Never writes a
# checkpoint or bitstream. Usage:
#   vivado -mode batch -nojournal -notrace -log probe.log -source vivado_probe.tcl \
#     -tclargs <route.dcp> <clone>/sw/litex/timing_grade.tcl <out-dir>
lassign $argv dcp hook out
set_param general.maxThreads 8
open_checkpoint $dcp
source $hook
kl_timing_grade_configure xc7a100t-fgg484-2 commercial 0 85 {Slow Fast}

proc slack1 {type} {
    set p [get_timing_paths -delay_type $type -max_paths 1]
    return [format %.3f [get_property SLACK $p]]
}
proc corner_only {c} {
    foreach x {Slow Fast} {
        config_timing_corners -corner $x -delay_type [expr {$x eq $c ? "min_max" : "none"}]
    }
}

# P1: does grade or junction temperature change any timing number?
set rows {}
foreach cond {{commercial 0} {commercial 85} {commercial 25} {industrial -40} {industrial 100} {extended 100}} {
    lassign $cond g t
    if {[catch {set_operating_conditions -grade $g -junction_temp $t} msg]} {
        lappend rows "P1 grade=$g tj=$t not-accepted: [lindex [split $msg \n] 0]"
        continue
    }
    set got [report_operating_conditions -grade -junction_temp -return_string]
    lappend rows "P1 grade=$g tj=$t tool-reports: [string map {\n { | }} [string trim $got]]"
    foreach c {Slow Fast} {
        corner_only $c
        lappend rows "P1 grade=$g tj=$t corner=$c WNS=[slack1 max] WHS=[slack1 min]"
    }
}
set_operating_conditions -grade commercial -junction_temp 85
foreach x {Slow Fast} {config_timing_corners -corner $x -delay_type min_max}
lappend rows "P1 both-corners commercial 85 WNS=[slack1 max] WHS=[slack1 min]"

# P2: live refusal controls in the real tool (restore after each).
foreach {label mutate} {
    grade-industrial {set_operating_conditions -grade industrial}
    tj-25            {set_operating_conditions -junction_temp 25}
    tj-0             {set_operating_conditions -junction_temp 0}
    fast-max-only    {config_timing_corners -corner Fast -delay_type max}
    slow-min-only    {config_timing_corners -corner Slow -delay_type min}
    fast-none        {config_timing_corners -corner Fast -delay_type none}
} {
    eval $mutate
    set rc [catch {kl_timing_grade_check} msg]
    lappend rows "P2 $label refused=$rc msg=[lindex [split $msg \n] 0]"
    set_operating_conditions -grade commercial -junction_temp 85
    foreach x {Slow Fast} {config_timing_corners -corner $x -delay_type min_max}
}
lappend rows "P2 restored-good refused=[catch {kl_timing_grade_check} msg]"
lappend rows "P2 report_config_timing: [string map {\n { | }} [report_config_timing -return_string]]"

# P3: the shipped XDC named clocks that do not exist; list the real clock names.
lappend rows "P3 clocks: [lsort [get_clocks]]"
lappend rows "P3 crg_clkout0 matches: [llength [get_clocks -quiet crg_clkout0]]"
lappend rows "P3 mr_ff cells: [llength [get_cells -hierarchical -quiet -filter {mr_ff == TRUE}]]"
lappend rows "P3 quasi_static cells: [llength [get_cells -hierarchical -quiet -filter {quasi_static == yes}]]"
# Bound the eth <-> sys/milan crossings as sw/litex/milan_soc.py:1499-1534 intends
# (8 ns datapath-only) and see what the shipping placement actually gives.
set eth [get_clocks eth_clocks0_rx]
set sysm [get_clocks {milansoc_crg_clkout0 milansoc_crg_clkout1}]
set rc [catch {reset_path -to [get_cells -hierarchical -filter {mr_ff == TRUE}]} msg]
lappend rows "P3 mr_ff false paths still reported after reset: [llength [get_timing_paths -quiet -from $eth -to [get_clocks milansoc_crg_clkout0] -max_paths 5]]"
lappend rows "P3 reset_path mr_ff rc=$rc $msg"
foreach {a b} [list $eth $sysm $sysm $eth] {
    set_max_delay -datapath_only -from $a -to $b 8.000
}
foreach c {Slow Fast} {
    corner_only $c
    foreach {a b} [list eth_clocks0_rx milansoc_crg_clkout0 milansoc_crg_clkout0 eth_clocks0_rx \
                        eth_clocks0_rx milansoc_crg_clkout1 milansoc_crg_clkout1 eth_clocks0_rx] {
        set ps [get_timing_paths -from [get_clocks $a] -to [get_clocks $b] -delay_type max -max_paths 200 -nworst 1]
        set n [llength $ps]
        if {$n == 0} { lappend rows "P3 $c $a->$b paths=0"; continue }
        set worst [lindex $ps 0]
        if {[get_property SLACK $worst] eq ""} {
            lappend rows "P3 $c $a->$b paths=$n worst=UNCONSTRAINED exc=[get_property EXCEPTION $worst] start=[get_property STARTPOINT_PIN $worst] end=[get_property ENDPOINT_PIN $worst]"
            continue
        }
        set dmax 0.0
        set dmin 1e9
        foreach p $ps {
            set d [get_property DATAPATH_DELAY $p]
            if {$d > $dmax} {set dmax $d}
            if {$d < $dmin} {set dmin $d}
        }
        lappend rows [format "P3 %s %s->%s paths=%d worst_slack=%.3f req=%s datapath_max=%.3f datapath_min=%.3f exc=%s" \
            $c $a $b $n [get_property SLACK $worst] [get_property REQUIREMENT $worst] $dmax $dmin \
            [get_property EXCEPTION $worst]]
    }
}
report_timing -from [get_clocks eth_clocks0_rx] -to [get_clocks milansoc_crg_clkout0] -max_paths 20 -nworst 1 \
    -file $out/bounded_eth_to_sys.rpt
report_timing -from [get_clocks milansoc_crg_clkout0] -to [get_clocks eth_clocks0_rx] -max_paths 20 -nworst 1 \
    -file $out/bounded_sys_to_eth.rpt

set f [open $out/probe-results.txt w]
foreach r $rows {puts $f $r; puts $r}
close $f
exit
