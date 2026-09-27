set_param general.maxThreads 16
foreach command {config_timing_corners report_timing_summary get_timing_paths report_operating_conditions report_cdc report_clock_interaction report_timing check_timing} {
    puts [help $command]
}
exit
