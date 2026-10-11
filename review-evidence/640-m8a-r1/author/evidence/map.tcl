# M8a memory-fit mapping: one OOC synthesis per LiteX memory instance, shipping part and directive.
set mods [lindex $argv 0]
set out [open ../map.tsv w]
puts $out "module\tdepth_words\tRAMB36E1\tRAMB18E1\tLUT\tFF\tLUTRAM"
foreach m $mods {
  read_verilog $m.v
  synth_design -top $m -part xc7a100t-fgg484-2 -mode out_of_context -directive AreaOptimized_high
  set r36 [llength [get_cells -quiet -hier -filter {REF_NAME == RAMB36E1}]]
  set r18 [llength [get_cells -quiet -hier -filter {REF_NAME == RAMB18E1}]]
  set lut [llength [get_cells -quiet -hier -filter {PRIMITIVE_GROUP == LUT}]]
  set ff [llength [get_cells -quiet -hier -filter {PRIMITIVE_GROUP == FLOP_LATCH}]]
  set lutram [llength [get_cells -quiet -hier -filter {PRIMITIVE_GROUP == DMEM}]]
  set depth [exec grep -o {mem\[0:[0-9]*\]} $m.v]
  puts $out "$m\t$depth\t$r36\t$r18\t$lut\t$ff\t$lutram"
  flush $out
  report_utilization -file ../util_$m.rpt
  close_design
  close_project -quiet
}
close $out
