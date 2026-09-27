# Reviewer probe: what the per-build power report says with the operating conditions
# as shipped (auto Tj) versus as the new platform hook pins them (commercial, Tj 85).
#   vivado -mode batch -nojournal -notrace -log power.log -source power_probe.tcl -tclargs <route.dcp copy> <timing_grade.tcl>
set_param general.maxThreads 8
lassign $argv dcp hook
open_checkpoint $dcp
report_power -file power_as_shipped.rpt
source $hook
kl_timing_grade_configure xc7a100t-fgg484-2 commercial 0 85 {Slow Fast}
report_power -file power_hook_pinned.rpt
set_operating_conditions -junction_temp auto -ambient_temp 50
report_power -file power_auto_ambient50.rpt
puts "POWER FINISHED"
exit
