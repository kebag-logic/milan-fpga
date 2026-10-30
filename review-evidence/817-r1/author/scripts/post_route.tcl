# #817: read-only reports on a routed checkpoint, run identically on dev's and the head's route.
# The servo PS reset synchronizer crossing as timed (setup and hold), the exceptions on its D pin, every
# milan -> PS clock endpoint with its slack and exception, the CDC report for that pair and for the design,
# ignored exceptions, and the 10 worst setup and hold paths over every path group. Nothing is written back.
# usage: vivado -mode batch -source post_route.tcl -tclargs <routed.dcp> <outdir>
lassign $argv dcp out
set_param general.maxThreads 8
file mkdir $out
open_checkpoint $dcp
set first [get_cells -hierarchical -filter {NAME =~ "*mmcm_servo/psrst_sync_r_reg[0]"}]
set stages [get_cells -hierarchical -filter {NAME =~ "*mmcm_servo/psrst_sync_r_reg*"}]
set dpin [get_pins -of_objects $first -filter {REF_PIN_NAME == D}]
set ps [get_clocks -of_objects [get_pins -of_objects $first -filter {IS_CLOCK == 1}]]
set milan [get_clocks -of_objects [get_nets milansoc_crg_clkout1]]
set fh [open $out/crossing.txt w]
puts $fh "milan_clock=$milan ps_clock=$ps"
foreach c [lsort $stages] {
    puts $fh "$c ASYNC_REG=[get_property ASYNC_REG $c] LOC=[get_property LOC $c] BEL=[get_property BEL $c]"
}
foreach kind {max min} {
    set p [get_timing_paths -to $dpin -delay_type $kind -max_paths 1]
    puts $fh "$kind: slack=[get_property SLACK $p] requirement=[get_property REQUIREMENT $p] exception=[get_property EXCEPTION $p] datapath_delay=[get_property DATAPATH_DELAY $p] levels=[get_property LOGIC_LEVELS $p] start=[get_property STARTPOINT_PIN $p] start_clock=[get_property STARTPOINT_CLOCK $p] end_clock=[get_property ENDPOINT_CLOCK $p]"
}
close $fh
report_timing -to $dpin -delay_type max -input_pins -file $out/crossing_setup.rpt
report_timing -to $dpin -delay_type min -input_pins -file $out/crossing_hold.rpt
report_exceptions -to $dpin -file $out/crossing_exceptions.rpt
report_exceptions -ignored -file $out/exceptions_ignored.rpt
report_clock_interaction -delay_type min_max -from $milan -to $ps -file $out/clock_interaction_milan_ps.rpt
report_cdc -from $milan -to $ps -summary -file $out/cdc_milan_ps_summary.rpt
report_cdc -from $milan -to $ps -details -file $out/cdc_milan_ps_details.rpt
report_cdc -summary -file $out/cdc_design_summary.rpt
# every endpoint of the milan -> PS clock pair, setup, worst path each (false paths included)
set fh [open $out/milan_ps_endpoints.tsv w]
puts $fh "endpoint\tslack\trequirement\texception\tlevels\tdatapath_delay\tstartpoint"
foreach p [get_timing_paths -from $milan -to $ps -delay_type max -max_paths 1000 -nworst 1 -unique_pins] {
    puts $fh "[get_property ENDPOINT_PIN $p]\t[get_property SLACK $p]\t[get_property REQUIREMENT $p]\t[get_property EXCEPTION $p]\t[get_property LOGIC_LEVELS $p]\t[get_property DATAPATH_DELAY $p]\t[get_property STARTPOINT_PIN $p]"
}
set p [get_timing_paths -to $dpin -delay_type max -max_paths 1]
puts $fh "[get_property ENDPOINT_PIN $p]\t[get_property SLACK $p]\t[get_property REQUIREMENT $p]\t[get_property EXCEPTION $p]\t[get_property LOGIC_LEVELS $p]\t[get_property DATAPATH_DELAY $p]\t[get_property STARTPOINT_PIN $p]\t(queried by pin)"
close $fh
# the 10 worst setup and hold paths over every path group, one per endpoint
foreach kind {max min} {
    set fh [open $out/top10_$kind.tsv w]
    puts $fh "rank\tslack\tstart_clock\tend_clock\tlevels\tdatapath_delay\tlogic_delay\texception\tstartpoint\tendpoint"
    set rank 0
    foreach p [get_timing_paths -delay_type $kind -max_paths 10 -nworst 1 -unique_pins -sort_by slack] {
        incr rank
        set ld [get_property -quiet DATAPATH_LOGIC_DELAY $p]
        puts $fh "$rank\t[get_property SLACK $p]\t[get_property STARTPOINT_CLOCK $p]\t[get_property ENDPOINT_CLOCK $p]\t[get_property LOGIC_LEVELS $p]\t[get_property DATAPATH_DELAY $p]\t$ld\t[get_property EXCEPTION $p]\t[get_property STARTPOINT_PIN $p]\t[get_property ENDPOINT_PIN $p]"
    }
    close $fh
    report_timing -delay_type $kind -max_paths 10 -nworst 1 -unique_pins -sort_by slack -file $out/top10_$kind.rpt
}
puts "POST-ROUTE-DONE"
