# SPDX-License-Identifier: CERN-OHL-W-2.0
# Place both test_gmii_rx_capture.py fixtures and grade the real IOB checker.
# The negative fixture must fail specifically at the nine pad-to-D paths.
# Usage: vivado -mode batch -source gmii_rx_capture_check.tcl -tclargs <emit-dir>
if {$argc != 1} { error "expected test_gmii_rx_capture.py --emit-dir directory" }
set fixtures [file normalize [lindex $argv 0]]
set here [file dirname [file normalize [info script]]]
source [file join $here iob_pack_check.tcl]
set_param general.maxThreads 4

foreach case_name {capture reset_before_d} {
    set source_file [file join $fixtures ${case_name}.v]
    if {![file isfile $source_file]} { error "missing fixture: $source_file" }
    set result_dir [file join $fixtures $case_name]
    file mkdir $result_dir
    cd $result_dir
    # The checker also reads the constraints beside its report.
    file copy -force [file join $here gmii_rx_capture.xdc] capture.xdc
    create_project -in_memory -part xc7a100t-fgg484-2
    read_verilog $source_file
    read_xdc capture.xdc
    synth_design -top gmii_capture -part xc7a100t-fgg484-2 -control_set_opt_threshold 100
    opt_design
    place_design
    set rejected [catch {kl_iob_pack_check capture_iob_pack.rpt} message]
    set fh [open capture_iob_pack.rpt r]
    set report [read $fh]
    close $fh
    set passes [regexp -all -line {^PASS  } $report]
    set failures [regexp -all -line {^FAIL  } $report]
    set inert [regexp -all -line {^INERT  } $report]
    if {$case_name eq "capture"} {
        if {$rejected || $passes != 9 || $failures != 0 || $inert != 0} {
            error "good fixture did not pack all nine inputs: $message"
        }
    } else {
        set blocked [regexp -all {IN, no register reads the pad, only:} $report]
        if {!$rejected || $passes != 0 || $failures != 9 || $inert != 0 || $blocked != 9
            || ![string match {IOB-PACK FAIL: 9 port(s)*} $message]} {
            error "reset-before-D control was not refused on all nine inputs: $message"
        }
        puts "Expected refusal: $message"
    }
    close_project
}
puts "GMII capture placement: 9 PASS / 9 expected FAIL"
