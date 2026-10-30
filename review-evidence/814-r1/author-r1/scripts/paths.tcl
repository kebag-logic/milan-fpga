# #814: the routed checkpoint's top sys-domain setup paths, read without changing the netlist.
# Run in the checkpoint's directory. Writes sys_paths.tsv (worst path per endpoint, up to 5,000 endpoints:
# slack, logic levels, data-path delay, its routing part, start and end pins) and sys_top20.rpt (full detail).
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
report_timing_summary -no_detailed_paths -file timing_summary_reopen.rpt
quit
