# #814: the routed checkpoint's top sys-domain setup paths, read without changing the netlist.
# Run in the checkpoint's directory. Writes sys_paths.tsv (worst path per endpoint, up to 5,000 endpoints:
# slack, logic levels, data-path delay, its routing part, start and end pins), sys_top20.rpt (full detail), the same
# over every path group (all_paths.tsv, all_top30.rpt; round 2) and
# stage_cells.tsv (round 2: the cells named for each #814 stage, by primitive kind, and the slices they occupy).
set_param general.maxThreads 16
open_checkpoint alinx_ax7101_route.dcp
set group milansoc_crg_clkout0
set paths [get_timing_paths -setup -group $group -max_paths 5000 -nworst 1 -sort_by slack]
set f [open sys_paths.tsv w]
puts $f "slack_ns\tlevels\tdata_ns\troute_ns\tstart\tend"
foreach p $paths {
  puts $f "[get_property SLACK $p]\t[get_property LOGIC_LEVELS $p]\t[get_property DATAPATH_DELAY $p]\t[get_property DATAPATH_NET_DELAY $p]\t[get_property STARTPOINT_PIN $p]\t[get_property ENDPOINT_PIN $p]"
}
close $f
report_timing -setup -group $group -max_paths 20 -nworst 1 -input_pins -file sys_top20.rpt
# round 2: the same over every path group, since the worst path need not be a sys path
set paths [get_timing_paths -setup -max_paths 5000 -nworst 1 -sort_by slack]
set f [open all_paths.tsv w]
puts $f "slack_ns\tlevels\tdata_ns\troute_ns\tstart\tend\tgroup\tstart_clock\tend_clock"
foreach p $paths {
  puts $f "[get_property SLACK $p]\t[get_property LOGIC_LEVELS $p]\t[get_property DATAPATH_DELAY $p]\t[get_property DATAPATH_NET_DELAY $p]\t[get_property STARTPOINT_PIN $p]\t[get_property ENDPOINT_PIN $p]\t[get_property GROUP $p]\t[get_property STARTPOINT_CLOCK $p]\t[get_property ENDPOINT_CLOCK $p]"
}
close $f
report_timing -setup -max_paths 30 -nworst 1 -input_pins -file all_top30.rpt
report_timing_summary -no_detailed_paths -file timing_summary_reopen.rpt
set f [open stage_cells.tsv w]
puts $f "stage\tpattern\tFF\tLUT\tother\tslices"
foreach {stage pattern} {F1 *stage_spi_phy* F2 *pipeready* F3 *refresher_cmd*} {
  set cells [get_cells -hier -quiet -filter "IS_PRIMITIVE && NAME =~ $pattern"]
  set ff [llength [filter -quiet $cells {REF_NAME =~ FD*}]]
  set lut [llength [filter -quiet $cells {REF_NAME =~ LUT*}]]
  set other [expr {[llength $cells] - $ff - $lut}]
  set slices [llength [lsort -unique [get_sites -quiet -of_objects $cells -filter {SITE_TYPE =~ SLICE*}]]]
  puts $f "$stage\t$pattern\t$ff\t$lut\t$other\t$slices"
}
close $f
quit
