# argv: 0 = promote (1) or not (0); 1 = image path handed to HEX_P
set_param general.maxThreads 2
set promote [lindex $argv 0]
set hex [lindex $argv 1]
read_verilog -sv [file join [file dirname [info script]] rom_probe.sv]
if {$promote} { set_msg_config -id {Synth 8-4445} -new_severity ERROR }
synth_design -top rom_probe -part xc7a100t-fgg484-2 -mode out_of_context -generic "HEX_P=\"$hex\""
report_utilization -file util.rpt
puts "PROBE-REACHED-END"
