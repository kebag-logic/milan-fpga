read_verilog -sv [list hdl/milan/mailbox/KL_mbx_pkg.sv hdl/milan/mailbox/KL_mbx_ring.sv \
  hdl/milan/mailbox/KL_mbx_rx.sv hdl/milan/mailbox/KL_mbx_tx.sv hdl/milan/mailbox/KL_mbx_evt.sv \
  hdl/milan/mailbox/KL_mbx.sv hdl/milan/mailbox/KL_mbx_wb.sv hdl/milan/mailbox/KL_mbx_axil.sv \
  tb/verilator/mbx/tb_mbx_top.sv]
synth_design -mode out_of_context -top tb_mbx_top -part xc7a100tfgg484-2 -generic HOST_P=0
create_clock -period 10.000 -name clk [get_ports clk_i]
opt_design
place_design
route_design
report_utilization -hierarchical -file util_hier.rpt
report_utilization -file util.rpt
report_timing_summary -delay_type max -file timing.rpt
report_route_status -file route.rpt
