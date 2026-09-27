set_param general.maxThreads 16
foreach command {config_timing_corners report_timing_summary get_timing_paths report_operating_conditions report_cdc report_clock_interaction report_timing check_timing} {
    help $command
}
open_checkpoint $WORKSPACE_HOME/litex-milan/work/build_ax7101_eto_tdm8dev9e9954e9/gateware/alinx_ax7101_route.dcp
report_property [current_design]
report_property [get_parts [get_property PART [current_design]]]
report_operating_conditions
report_timing_summary -delay_type min_max -report_unconstrained -max_paths 1 -file $VALIDATION_STORAGE/395-a387-work/baseline_timing.rpt
exit
