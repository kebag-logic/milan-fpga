set_param general.maxThreads 1
open_checkpoint {$WORKSPACE_HOME/litex-milan/work/build_ax7101_eto_tdm8dev9e9954e9/gateware/alinx_ax7101_route.dcp}
source {$LANES/395-timing-grade/sw/litex/timing_grade.tcl}
kl_timing_grade_configure {xc7a100t-fgg484-2} {commercial} {0} {85} {Slow Fast}

proc expect_refusal {label script reason} {
    if {![catch {uplevel 1 $script} message]} {
        error "CONTROL $label unexpectedly accepted"
    }
    if {[string first $reason $message] < 0} {
        error "CONTROL $label wrong refusal: $message"
    }
    puts "CONTROL $label refused: $message"
}
kl_timing_grade_check
expect_refusal part {kl_timing_grade_configure xc7a100t-fgg484-1 commercial 0 85 {Slow Fast}} {part mismatch}
set_operating_conditions -grade industrial
expect_refusal grade {kl_timing_grade_check} {operating conditions changed}
set_operating_conditions -grade commercial -junction_temp 0
expect_refusal temperature {kl_timing_grade_check} {operating conditions changed}
set_operating_conditions -junction_temp 85
foreach corner {Slow Fast} {
    foreach delays {none min max} {
        config_timing_corners -corner $corner -delay_type $delays
        expect_refusal "$corner-$delays" {kl_timing_grade_check} {requires setup and hold}
        config_timing_corners -corner $corner -delay_type min_max
    }
}
kl_timing_grade_check
puts "LIVE CONTROLS: nine wrong-condition refusals, declaration restored"
exit
