foreach d {5 7} {
  read_verilog -sv <repo>/hdl/ieee1722/aaf/KL_render_setpoint.sv
  synth_design -mode out_of_context -top KL_render_setpoint -part xc7a100tfgg484-2 -directive AreaOptimized_high \
    -generic N_STREAMS_P=1 -generic N_CH_P=8 -generic DEPTH_LOG2_P=$d -generic PDU_EVENTS_P=6 -generic SETPOINT_EVT_P=8 \
    -generic CONV_BAND_EVT_P=3 -generic RESET_BAND_EVT_P=6 -generic CLK_FREQ_HZ_P=50000000
  report_utilization -file util_d$d.rpt
  close_design
}
