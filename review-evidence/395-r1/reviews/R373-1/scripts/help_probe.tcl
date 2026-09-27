# Capture the tool's own command reference for the commands the hook relies on.
foreach c {set_operating_conditions report_operating_conditions config_timing_corners config_timing_analysis report_config_timing} {
    puts "===== HELP $c"
    if {[catch {puts [help $c]} m]} {puts "HELP-ERROR $c: $m"}
}
exit
