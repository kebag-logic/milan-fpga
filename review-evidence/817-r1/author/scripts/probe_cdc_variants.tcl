# #817: read-only probe of how report_cdc classifies the servo PS reset synchroniser crossing
# under candidate constraints. Each variant reopens the routed checkpoint; nothing is written
# back. Variants: fp_pin (false path from the milan clock to the first flop's D pin), fp_cell
# (to the first flop), mdd (set_max_delay -datapath_only 5.0 to the D pin), and the diagnostic
# async_groups (the two clocks declared asynchronous), each with ASYNC_REG on both flops, plus
# async_groups_noattr without ASYNC_REG.
# usage: vivado -mode batch -source probe_cdc_variants.tcl -tclargs <routed.dcp> <outdir>
lassign $argv dcp out
set_param general.maxThreads 8
file mkdir $out
foreach variant {fp_pin fp_cell mdd async_groups async_groups_noattr} {
    open_checkpoint $dcp
    set sync [get_cells -hierarchical -filter {NAME =~ "*/g_mmcm_servo.mmcm_servo/psrst_sync_r_reg*"}]
    set first {}
    foreach c $sync {if {[string match {*_reg\[0\]} $c]} {lappend first $c}}
    set first [get_cells $first]
    set dpin [get_pins -of_objects $first -filter {REF_PIN_NAME == D}]
    set dst [get_clocks -of_objects [get_pins -of_objects $first -filter {IS_CLOCK == 1}]]
    set src [get_clocks milansoc_crg_clkout1]
    if {$variant ne "async_groups_noattr"} {set_property ASYNC_REG TRUE $sync}
    switch $variant {
        fp_pin {set_false_path -from $src -to $dpin}
        fp_cell {set_false_path -from $src -to $first}
        mdd {set_max_delay 5.000 -datapath_only -from $src -to $dpin}
        default {set_clock_groups -asynchronous -group $src -group $dst}
    }
    report_cdc -from $src -to $dst -summary -file $out/$variant-cdc-summary.rpt
    report_cdc -from $src -to $dst -details -file $out/$variant-cdc-details.rpt
    report_cdc -details -file $out/$variant-cdc-all-details.rpt
    report_timing -to $dpin -delay_type max -file $out/$variant-timing-setup.rpt
    report_exceptions -to $dpin -file $out/$variant-exceptions.rpt
    set p [get_timing_paths -to $dpin -max_paths 1]
    puts "VARIANT $variant src=$src dst=$dst slack=[get_property SLACK $p] exception=[get_property EXCEPTION $p]"
    close_design
}
puts "PROBE-DONE"
