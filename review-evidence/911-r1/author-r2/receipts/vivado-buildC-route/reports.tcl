# Raw per-corner timing summary and CDC report of build C's routed design (the image commit 1e604e1b), read from
# its routed checkpoint (written after post-route phys_opt, the design the signoff hook reported). No rebuild.
# The operating conditions are set by the image commit's own timing_grade.tcl with the arguments build C's
# script passed (alinx_ax7101.tcl:293); each corner then runs report_timing_summary as the signoff hook does
# (timing_grade.tcl kl_timing_grade_reports) with detailed paths left out so the report stays small.
set_param general.maxThreads 8
open_checkpoint ../../buildC/gateware/alinx_ax7101_route.dcp
source ../../C/sw/litex/timing_grade.tcl
kl_timing_grade_configure {xc7a200t-fbg484-2} {commercial} {0} {85} {Slow Fast}
kl_timing_grade_check
set spec $::kl_timing_grade
foreach temp [list [dict get $spec min_c] [dict get $spec max_c]] {
    set_operating_conditions -junction_temp $temp
    foreach corner [dict get $spec corners] {
        config_timing_corners -corner $corner -delay_type min_max
        foreach other [dict get $spec corners] {
            if {$other ne $corner} { config_timing_corners -corner $other -delay_type none }
        }
        set stem out/buildC_route_${corner}_${temp}C
        report_operating_conditions -file ${stem}_operating.rpt
        report_timing_summary -delay_type min_max -report_unconstrained \
            -no_detailed_paths -file ${stem}_timing_summary.rpt
    }
}
set_operating_conditions -junction_temp [dict get $spec max_c]
foreach corner [dict get $spec corners] { config_timing_corners -corner $corner -delay_type min_max }
kl_timing_grade_check
report_timing_summary -delay_type min_max -report_unconstrained -no_detailed_paths \
    -file out/buildC_route_all_timing_summary.rpt
report_cdc -file out/buildC_route_cdc_summary.rpt
report_cdc -details -file out/buildC_route_cdc_details.rpt
puts "R2-REPORTS-DONE"
