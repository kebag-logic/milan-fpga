set_msg_config -id {Synth 8-4445} -new_severity ERROR
set out [open ctrl_memory_ooc.tsv w]
puts $out "top	RAMB36E1	RAMB18E1	LUT	FF	LUTRAM"
read_verilog s1i1_rom.v
synth_design -top s1i1_rom -part xc7a100t-fgg484-2 -mode out_of_context -directive AreaOptimized_high
set n {}
foreach f {{REF_NAME == RAMB36E1} {REF_NAME == RAMB18E1} {PRIMITIVE_GROUP == LUT} {PRIMITIVE_GROUP == FLOP_LATCH} {PRIMITIVE_GROUP == DMEM}} {
  lappend n [llength [get_cells -quiet -hier -filter $f]]
}
puts $out "s1i1_rom\t[join $n \t]"
report_utilization -file s1i1_rom_utilization.rpt
close_design
close_project -quiet
read_verilog s1i1_sram.v
synth_design -top s1i1_sram -part xc7a100t-fgg484-2 -mode out_of_context -directive AreaOptimized_high
set n {}
foreach f {{REF_NAME == RAMB36E1} {REF_NAME == RAMB18E1} {PRIMITIVE_GROUP == LUT} {PRIMITIVE_GROUP == FLOP_LATCH} {PRIMITIVE_GROUP == DMEM}} {
  lappend n [llength [get_cells -quiet -hier -filter $f]]
}
puts $out "s1i1_sram\t[join $n \t]"
report_utilization -file s1i1_sram_utilization.rpt
close_design
close_project -quiet
read_verilog s1i2_rom.v
synth_design -top s1i2_rom -part xc7a100t-fgg484-2 -mode out_of_context -directive AreaOptimized_high
set n {}
foreach f {{REF_NAME == RAMB36E1} {REF_NAME == RAMB18E1} {PRIMITIVE_GROUP == LUT} {PRIMITIVE_GROUP == FLOP_LATCH} {PRIMITIVE_GROUP == DMEM}} {
  lappend n [llength [get_cells -quiet -hier -filter $f]]
}
puts $out "s1i2_rom\t[join $n \t]"
report_utilization -file s1i2_rom_utilization.rpt
close_design
close_project -quiet
read_verilog s1i2_sram.v
synth_design -top s1i2_sram -part xc7a100t-fgg484-2 -mode out_of_context -directive AreaOptimized_high
set n {}
foreach f {{REF_NAME == RAMB36E1} {REF_NAME == RAMB18E1} {PRIMITIVE_GROUP == LUT} {PRIMITIVE_GROUP == FLOP_LATCH} {PRIMITIVE_GROUP == DMEM}} {
  lappend n [llength [get_cells -quiet -hier -filter $f]]
}
puts $out "s1i2_sram\t[join $n \t]"
report_utilization -file s1i2_sram_utilization.rpt
close_design
close_project -quiet
read_verilog s8i1_rom.v
synth_design -top s8i1_rom -part xc7a100t-fgg484-2 -mode out_of_context -directive AreaOptimized_high
set n {}
foreach f {{REF_NAME == RAMB36E1} {REF_NAME == RAMB18E1} {PRIMITIVE_GROUP == LUT} {PRIMITIVE_GROUP == FLOP_LATCH} {PRIMITIVE_GROUP == DMEM}} {
  lappend n [llength [get_cells -quiet -hier -filter $f]]
}
puts $out "s8i1_rom\t[join $n \t]"
report_utilization -file s8i1_rom_utilization.rpt
close_design
close_project -quiet
read_verilog s8i1_sram.v
synth_design -top s8i1_sram -part xc7a100t-fgg484-2 -mode out_of_context -directive AreaOptimized_high
set n {}
foreach f {{REF_NAME == RAMB36E1} {REF_NAME == RAMB18E1} {PRIMITIVE_GROUP == LUT} {PRIMITIVE_GROUP == FLOP_LATCH} {PRIMITIVE_GROUP == DMEM}} {
  lappend n [llength [get_cells -quiet -hier -filter $f]]
}
puts $out "s8i1_sram\t[join $n \t]"
report_utilization -file s8i1_sram_utilization.rpt
close_design
close_project -quiet
read_verilog s8i2_rom.v
synth_design -top s8i2_rom -part xc7a100t-fgg484-2 -mode out_of_context -directive AreaOptimized_high
set n {}
foreach f {{REF_NAME == RAMB36E1} {REF_NAME == RAMB18E1} {PRIMITIVE_GROUP == LUT} {PRIMITIVE_GROUP == FLOP_LATCH} {PRIMITIVE_GROUP == DMEM}} {
  lappend n [llength [get_cells -quiet -hier -filter $f]]
}
puts $out "s8i2_rom\t[join $n \t]"
report_utilization -file s8i2_rom_utilization.rpt
close_design
close_project -quiet
read_verilog s8i2_sram.v
synth_design -top s8i2_sram -part xc7a100t-fgg484-2 -mode out_of_context -directive AreaOptimized_high
set n {}
foreach f {{REF_NAME == RAMB36E1} {REF_NAME == RAMB18E1} {PRIMITIVE_GROUP == LUT} {PRIMITIVE_GROUP == FLOP_LATCH} {PRIMITIVE_GROUP == DMEM}} {
  lappend n [llength [get_cells -quiet -hier -filter $f]]
}
puts $out "s8i2_sram\t[join $n \t]"
report_utilization -file s8i2_sram_utilization.rpt
close_design
close_project -quiet
close $out
