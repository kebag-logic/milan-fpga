# SPDX-License-Identifier: CERN-OHL-W-2.0
# Report the fixed speed models; changing power Tj does not prorate Artix-7 timing.
# All device/grade/range values arrive from platforms/ax7101_timing.py.

proc kl_timing_grade_configure {part grade min_c max_c corners} {
    set expected [get_property NAME [get_parts $part]]
    set actual [get_property PART [current_design]]
    if {$expected eq "" || $actual ne $expected} {
        error "TIMING-GRADE part mismatch: expected $part, found $actual"
    }
    set ::kl_timing_grade [dict create part $expected grade $grade \
        min_c $min_c max_c $max_c corners $corners]
    set_operating_conditions -grade $grade -junction_temp $max_c
    foreach corner $corners {
        config_timing_corners -corner $corner -delay_type min_max
    }
}

proc kl_timing_grade_check {} {
    set spec $::kl_timing_grade
    if {[get_property PART [current_design]] ne [dict get $spec part]} {
        error "TIMING-GRADE part changed after configuration"
    }
    set conditions [report_operating_conditions -grade -junction_temp -return_string]
    if {![regexp {Device Grade = (\S+)} $conditions -> grade] ||
        $grade ne [dict get $spec grade] ||
        ![regexp {Junction Temp = ([0-9.]+)} $conditions -> temp] ||
        $temp != [dict get $spec max_c]} {
        error "TIMING-GRADE operating conditions changed: $conditions"
    }
    set settings [report_config_timing -return_string]
    foreach corner [dict get $spec corners] {
        if {![regexp -line "^ *$corner +Yes +Yes *$" $settings]} {
            error "TIMING-GRADE requires setup and hold at $corner: $settings"
        }
    }
}

proc kl_timing_grade_reports {prefix} {
    kl_timing_grade_check
    set spec $::kl_timing_grade
    set info [open ${prefix}_grade.txt w]
    puts $info $spec
    puts $info "Fixed Slow/Fast timing models cover the declared range."
    puts $info "Endpoint Tj settings below are power metadata, not independent timing models."
    close $info
    # Analyse each supported model at both declared Tj endpoints, explicitly
    # retaining the identical results rather than claiming four PVT models.
    try {
        foreach temp [list [dict get $spec min_c] [dict get $spec max_c]] {
            set_operating_conditions -junction_temp $temp
            foreach corner [dict get $spec corners] {
                config_timing_corners -corner $corner -delay_type min_max
                foreach other [dict get $spec corners] {
                    if {$other ne $corner} {
                        config_timing_corners -corner $other -delay_type none
                    }
                }
                set stem ${prefix}_${corner}_${temp}C
                report_operating_conditions -file ${stem}_operating.rpt
                report_timing_summary -delay_type min_max -report_unconstrained \
                    -max_paths 5 -file ${stem}_timing.rpt
                report_timing -delay_type min_max -slack_lesser_than 0 \
                    -max_paths 100 -file ${stem}_negative.rpt
            }
        }
    } finally {
        set_operating_conditions -junction_temp [dict get $spec max_c]
        foreach corner [dict get $spec corners] {
            config_timing_corners -corner $corner -delay_type min_max
        }
    }
    kl_timing_grade_check
    report_timing_summary -delay_type min_max -report_unconstrained \
        -check_timing_verbose -max_paths 5 -file ${prefix}_all_timing.rpt
    report_clock_interaction -delay_type min_max -file ${prefix}_clock_interaction.rpt
    report_cdc -details -file ${prefix}_cdc.rpt
    check_timing -verbose -file ${prefix}_check_timing.rpt
}
