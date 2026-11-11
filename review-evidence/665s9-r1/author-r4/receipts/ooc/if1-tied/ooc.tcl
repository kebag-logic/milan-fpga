head e16c1343057ca23e544f22c4c023065809c3b5bf
command: tools/ooc_term.sh
full log: 556 bytes, sha256 c223980fff146a42c965b310c884556b6a1e47164a21453057cfc066a0b64a15
---
read_verilog -sv [list src/KL_mbx_pkg.sv src/KL_mbx_ring.sv src/KL_mbx_rx.sv src/KL_mbx_tx.sv src/KL_mbx_evt.sv   src/KL_mbx.sv src/KL_mbx_wb.sv src/KL_mbx_axil.sv src/tb_mbx_top.sv]
synth_design -mode out_of_context -top tb_mbx_top -part xc7a100tfgg484-2 -generic HOST_P=0
create_clock -period 10.000 -name clk [get_ports clk_i]
opt_design
place_design
route_design
report_utilization -hierarchical -file util_hier.rpt
report_utilization -file util.rpt
report_timing_summary -delay_type min_max -file timing.rpt
report_route_status -file route_status.rpt
