# #817: read-only probe of a routed checkpoint. Reports the servo PS reset synchroniser
# crossing as it is timed, its cells and properties, and the CDC classification of the
# milan -> PS clock pair. With PREVIEW=1 it then applies, in memory only, ASYNC_REG on both
# synchroniser flops and the false path into the first one, and reports again.
# The checkpoint is never written.
# usage: vivado -mode batch -source probe_dev.tcl -tclargs <routed.dcp> <outdir> <preview 0|1>
lassign $argv dcp out preview
set_param general.maxThreads 8
open_checkpoint $dcp
file mkdir $out
set sync [get_cells -hierarchical -quiet -filter {NAME =~ "*psrst_sync_r_reg*"}]
set fh [open $out/cells.txt w]
puts $fh "sync cells: [llength $sync]"
foreach c [get_cells -hierarchical -quiet -filter {NAME =~ "*mmcm_servo*" && IS_PRIMITIVE == 0}] {puts $fh "hier: $c"}
foreach c [lsort $sync] {
    puts $fh "$c REF_NAME=[get_property REF_NAME $c] ASYNC_REG=[get_property ASYNC_REG $c] LOC=[get_property LOC $c] BEL=[get_property BEL $c]"
    set clk [get_clocks -quiet -of_objects [get_pins -of_objects $c -filter {IS_CLOCK == 1}]]
    puts $fh "  clock=$clk"
    set dnet [get_nets -of_objects [get_pins -of_objects $c -filter {REF_PIN_NAME == D}]]
    set drv [get_pins -quiet -leaf -of_objects $dnet -filter {DIRECTION == OUT}]
    puts $fh "  D net=$dnet driver=$drv driver_ref=[get_property REF_NAME [get_cells -quiet -of_objects $drv]]"
    set drvcell [get_cells -quiet -of_objects $drv]
    if {[get_property REF_NAME $drvcell] ne "FDRE" && [get_property REF_NAME $drvcell] ne "FDPE"} {
        puts $fh "  driver INIT=[get_property -quiet INIT $drvcell]"
        foreach ip [get_pins -quiet -of_objects $drvcell -filter {DIRECTION == IN}] {
            set inet [get_nets -of_objects $ip]
            set idrv [get_pins -quiet -leaf -of_objects $inet -filter {DIRECTION == OUT}]
            puts $fh "    in $ip net=$inet driver=$idrv ref=[get_property REF_NAME [get_cells -quiet -of_objects $idrv]]"
        }
    }
}
close $fh
set first {}
foreach c $sync {if {[string match {*_reg\[0\]} $c]} {lappend first $c}}
set dpin [get_pins -of_objects $first -filter {REF_PIN_NAME == D}]
set psclk [get_clocks -of_objects [get_pins -of_objects $first -filter {IS_CLOCK == 1}]]
report_timing -to $dpin -max_paths 4 -nworst 4 -delay_type max -input_pins -file $out/timing_setup.rpt
report_timing -to $dpin -max_paths 4 -nworst 4 -delay_type min -input_pins -file $out/timing_hold.rpt
set paths [get_timing_paths -to $dpin -max_paths 1]
set srcclk [get_property STARTPOINT_CLOCK $paths]
set fh [open $out/clocks.txt w]
puts $fh "first=$first dpin=$dpin"
puts $fh "startpoint_clock=$srcclk endpoint_clock=$psclk"
puts $fh "slack=[get_property SLACK $paths] requirement=[get_property REQUIREMENT $paths] exception=[get_property EXCEPTION $paths] datapath_delay=[get_property DATAPATH_DELAY $paths] logic_levels=[get_property LOGIC_LEVELS $paths]"
close $fh
report_clock_interaction -delay_type min_max -from $srcclk -to $psclk -file $out/clock_interaction_pair.rpt
report_exceptions -to $dpin -file $out/exceptions_to_dpin.rpt
report_cdc -from $srcclk -to $psclk -details -file $out/cdc_pair.rpt
report_cdc -from $srcclk -to $psclk -summary -file $out/cdc_pair_summary.rpt
report_timing_summary -max_paths 10 -report_unconstrained -file $out/timing_summary.rpt
if {$preview} {
    set_property ASYNC_REG TRUE $sync
    set_false_path -from $srcclk -to $dpin
    report_timing -to $dpin -max_paths 4 -nworst 4 -delay_type max -input_pins -file $out/preview_timing_setup.rpt
    report_exceptions -to $dpin -file $out/preview_exceptions_to_dpin.rpt
    report_cdc -from $srcclk -to $psclk -details -file $out/preview_cdc_pair.rpt
    report_cdc -from $srcclk -to $psclk -summary -file $out/preview_cdc_pair_summary.rpt
}
puts "PROBE-DONE"
