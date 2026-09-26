# Arm A: the helper's promotion; arm B: no promotion (control).
set arm [lindex $argv 0]
set_param general.maxThreads 1
create_project -in_memory -part xc7a100t-fgg484-2
read_verilog -sv rom_probe.sv
if {$arm eq "promoted"} {
  set_msg_config -id {Synth 8-4445} -new_severity ERROR
}
synth_design -top rom_probe -part xc7a100t-fgg484-2 -mode out_of_context
report_utilization -file util_$arm.rpt
quit
