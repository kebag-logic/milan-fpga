# Reviewer probe (R590-1, #640 lane M2): out-of-context synthesis of one
# crossing harness. Usage: vivado -mode batch -source xing_ooc.tcl -tclargs <in.v> <outprefix>
set src [lindex $argv 0]
set out [lindex $argv 1]
set_param general.maxThreads 4
read_verilog $src
synth_design -top xing_top -part xc7a100tfgg484-2 -mode out_of_context -directive AreaOptimized_high
create_clock -name sys -period 10.0 [get_ports sys_clk]
create_clock -name milan -period 20.0 [get_ports milan_clk]
create_clock -name macsys -period 10.0 [get_ports macsys_clk]
create_clock -name macdp -period 20.0 [get_ports macdp_clk]
report_utilization -file ${out}_util.rpt
set fh [open ${out}_cells.tsv w]
foreach c [lsort [get_cells -hier -filter {IS_PRIMITIVE && (REF_NAME =~ RAMB* || REF_NAME =~ RAM32* || REF_NAME =~ RAM64*)}]] {
  set r [get_property REF_NAME $c]
  set wm ""
  if {[string match RAMB* $r]} {
    set wm "[get_property WRITE_MODE_A $c]/[get_property WRITE_MODE_B $c] RAM_MODE=[get_property RAM_MODE $c] DOA_REG=[get_property DOA_REG $c] DOB_REG=[get_property DOB_REG $c] WIDTHS=[get_property READ_WIDTH_A $c]/[get_property WRITE_WIDTH_B $c]"
  }
  puts $fh "$r\t$c\t$wm"
}
close $fh
report_drc -file ${out}_drc.rpt
report_methodology -file ${out}_methodology.rpt
