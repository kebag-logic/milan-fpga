# #817: run the repository's servo reset synchronizer hook against a real routed netlist, read-only.
# At dev the synchronizer has no ASYNC_REG, so the hook must refuse; with the attribute set in
# memory it must cut exactly the first stage's D pin from the milan clock. Nothing is written back.
# usage: vivado -mode batch -source live_hook.tcl -tclargs <routed.dcp> <clock_constraints.tcl> <milan net> <outdir>
lassign $argv dcp hooks milan out
set_param general.maxThreads 8
file mkdir $out
open_checkpoint $dcp
source $hooks
set rc [catch {kl_servo_reset_sync_constraints $milan} message]
puts "LIVE-DEV rc=$rc message=$message"
set stages [get_cells -hierarchical -filter {NAME =~ "*mmcm_servo/psrst_sync_r_reg*"}]
set_property ASYNC_REG TRUE $stages
set rc [catch {kl_servo_reset_sync_constraints $milan} message]
puts "LIVE-ATTR rc=$rc message=$message"
report_exceptions -file $out/live_attr_exceptions.rpt
set first [get_cells -hierarchical -filter {NAME =~ "*mmcm_servo/psrst_sync_r_reg[0]"}]
report_exceptions -to [get_pins -of_objects $first -filter {REF_PIN_NAME == D}] -file $out/live_attr_exceptions_to_dpin.rpt
report_timing -to [get_pins -of_objects $first -filter {REF_PIN_NAME == D}] -file $out/live_attr_timing.rpt
puts "LIVE-DONE"
