set_param general.maxThreads 8
open_checkpoint {<scratch>/viv/w/ax7101-AltSpreadLogic_high/alinx_ax7101_route.dcp}
source {<scratch>/viv/gclone/sw/litex/timing_grade.tcl}
kl_timing_grade_configure {xc7a100t-fgg484-2} {commercial} {0} {85} {Slow Fast}
set f [open {<scratch>/viv/paths/aslh/slacks.tsv} w]
puts $f "corner\tsetup_slack_ns\thold_slack_ns\tsetup_levels"
foreach temp {0 85} {
  set_operating_conditions -junction_temp $temp
  foreach corner {Slow Fast} {
    config_timing_corners -corner $corner -delay_type min_max
    foreach other {Slow Fast} { if {$other ne $corner} { config_timing_corners -corner $other -delay_type none } }
    set stem "<scratch>/viv/paths/aslh/${corner}_${temp}C"
    report_timing -delay_type max -max_paths 1 -nworst 1 -sort_by slack -input_pins -file ${stem}_worst_setup.rpt
    report_timing -delay_type min -max_paths 1 -nworst 1 -sort_by slack -input_pins -file ${stem}_worst_hold.rpt
    set s [get_timing_paths -delay_type max -max_paths 1 -nworst 1 -sort_by slack]
    set h [get_timing_paths -delay_type min -max_paths 1 -nworst 1 -sort_by slack]
    puts $f "${corner}_${temp}C\t[get_property SLACK $s]\t[get_property SLACK $h]\t[expr {[catch {get_property LOGIC_LEVELS $s} l] ? "na" : $l}]"
  }
}
close $f
exit
