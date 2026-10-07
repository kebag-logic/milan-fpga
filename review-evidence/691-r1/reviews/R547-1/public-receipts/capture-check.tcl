set case_name [lindex $argv 0]
if {$case_name ni {capture reset_before_d}} { error "expected fixture name" }
set_param general.maxThreads 4
create_project -in_memory -part xc7a100t-fgg484-2
read_verilog ../${case_name}.v
read_xdc capture.xdc
synth_design -top gmii_capture -part xc7a100t-fgg484-2 -control_set_opt_threshold 100
opt_design
place_design
write_checkpoint -force placed.dcp
source $::env(REPO)/sw/litex/iob_pack_check.tcl
kl_iob_pack_check capture_iob_pack.rpt
puts {ROUTING WOULD START}
