# #814: each stage alone, out of context on the shipping part with the shipping synthesis and opt directives,
# placed, for its own LUT, FF and slice counts. Run in the directory holding v/<top>.v; writes <top>_util.rpt.
set_param general.maxThreads 8
foreach top {spi_phy_stage axi_ready_stage refresher_staged refresher_plain} {
  create_project -in_memory -part xc7a100tfgg484-2
  read_verilog v/$top.v
  synth_design -top $top -part xc7a100tfgg484-2 -mode out_of_context -directive AreaOptimized_high
  create_clock -period 10.000 -name sys_clk [get_ports sys_clk]
  opt_design -directive ExploreArea
  place_design
  report_utilization -file ${top}_util.rpt
  close_project
}
quit
