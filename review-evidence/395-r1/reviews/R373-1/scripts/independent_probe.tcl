# Reviewer-owned probe for #395 / PR #605 at 66001a30.
# Usage (from an empty directory):
#   vivado -mode batch -nojournal -notrace -log probe.log \
#     -source independent_probe.tcl -tclargs <route.dcp copy> <checkout>/sw/litex/timing_grade.tcl
# Opens a COPY of the routed checkpoint, never writes a checkpoint or bitstream.
set_param general.maxThreads 8
lassign $argv dcp hook
open_checkpoint $dcp

# --- 1. Independent per-corner slack, not through the hook under review -------------
proc corner_only {corner} {
    foreach c {Slow Fast} {
        config_timing_corners -corner $c -delay_type [expr {$c eq $corner ? "min_max" : "none"}]
    }
}
proc all_corners {} {
    foreach c {Slow Fast} {config_timing_corners -corner $c -delay_type min_max}
}
proc worst {type} {
    set p [get_timing_paths -delay_type $type -max_paths 1 -nworst 1]
    if {[llength $p] == 0} {return "none"}
    return [format "%.3f %s %s" [get_property SLACK $p] [get_property CORNER $p] \
                [get_property DATAPATH_DELAY $p]]
}
proc tns {type} {
    # Sum of negative endpoint slack over every failing endpoint (0 if none).
    set paths [get_timing_paths -delay_type $type -max_paths 100000 -nworst 1 -slack_lesser_than 0]
    set s 0.0
    foreach p $paths {set s [expr {$s + [get_property SLACK $p]}]}
    return [format "%.3f %d" $s [llength $paths]]
}
proc snapshot {label} {
    set conds [string map {"\n" "; "} [report_operating_conditions -grade -junction_temp -return_string]]
    foreach corner {Slow Fast} {
        corner_only $corner
        puts "PROBE $label $corner setup=[worst max] tns=[tns max] hold=[worst min] ths=[tns min] | $conds"
    }
    all_corners
    puts "PROBE $label Both setup=[worst max] hold=[worst min]"
}

set part_obj [get_parts [get_property PART [current_design]]]
foreach prop {NAME SPEED TEMPERATURE_GRADE_LETTER} {
    if {[catch {get_property $prop $part_obj} v]} {set v "n/a"}
    puts "PROBE part.$prop=$v"
}
report_config_timing -file cfg_initial.rpt
snapshot as_opened

# --- 2. Temperature/grade sweep, including beyond the declared range -----------------
foreach {grade temp} {commercial 0 commercial 85 industrial -40 industrial 100 extended 100} {
    set_operating_conditions -grade $grade -junction_temp $temp
    snapshot "$grade/$temp"
}
set_operating_conditions -process maximum
snapshot "process-maximum"
set_operating_conditions -process typical
if {[catch {set_operating_conditions -voltage {Vccint 0.95}} m]} {puts "PROBE vccint-0.95 refused: $m"}
snapshot "vccint-0.95"
if {[catch {set_operating_conditions -voltage {Vccint 0.90}} m]} {puts "PROBE vccint-0.90 refused: $m"}
puts "PROBE after-vccint-0.90 part=[get_property PART [current_design]]"
snapshot "vccint-0.90"
reset_operating_conditions
puts "PROBE after-reset part=[get_property PART [current_design]]"

# --- 3. Reviewer-planted refusal controls against the real hook ----------------------
source $hook
proc expect_refusal {label script reason} {
    if {![catch {uplevel #0 $script} message]} {
        puts "CONTROL $label ACCEPTED (no refusal)"
        return
    }
    if {[string first $reason $message] < 0} {
        puts "CONTROL $label WRONG-REFUSAL: [string range $message 0 200]"
        return
    }
    puts "CONTROL $label refused: [string range [string map {"\n" " "} $message] 0 120]"
}
proc reconfigure {} {kl_timing_grade_configure xc7a100t-fgg484-2 commercial 0 85 {Slow Fast}}
expect_refusal other-device {kl_timing_grade_configure xc7a35t-fgg484-2 commercial 0 85 {Slow Fast}} {part mismatch}
expect_refusal nonexistent-part {kl_timing_grade_configure xc7a100t-nope-9 commercial 0 85 {Slow Fast}} {}
reconfigure
if {[catch {kl_timing_grade_check} m]} {puts "CONTROL baseline-check FAILED: $m"} else {puts "CONTROL baseline-check accepted"}
foreach {label cmd} {
    grade-extended   {set_operating_conditions -grade extended}
    temp-84.9        {set_operating_conditions -junction_temp 84.9}
    temp-100         {set_operating_conditions -junction_temp 100}
    temp-minus-40    {set_operating_conditions -junction_temp -40}
    temp-auto        {set_operating_conditions -junction_temp auto}
    both-setup-only  {config_timing_corners -delay_type max}
    fast-hold-flag   {config_timing_corners -corner Fast -hold}
    slow-setup-flag  {config_timing_corners -corner Slow -setup}
    reset-conditions {reset_operating_conditions}
} {
    uplevel #0 $cmd
    expect_refusal $label {kl_timing_grade_check} {TIMING-GRADE}
    reset_operating_conditions
    all_corners
    reconfigure
}
# Accepted-but-equivalent: 85.0 spelled differently must still pass.
set_operating_conditions -junction_temp 85.0
if {[catch {kl_timing_grade_check} m]} {puts "CONTROL equivalent-85.0 FAILED: $m"} else {puts "CONTROL equivalent-85.0 accepted"}
# Not in the hook's scope: analysis-wide settings that are not operating conditions.
config_timing_analysis -ignore_io_paths true
if {[catch {kl_timing_grade_check} m]} {puts "CONTROL ignore-io-paths refused"} else {puts "CONTROL ignore-io-paths ACCEPTED (outside hook scope)"}
config_timing_analysis -ignore_io_paths false
reconfigure
kl_timing_grade_check
puts "PROBE FINISHED"
exit
