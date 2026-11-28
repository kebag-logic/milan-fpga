// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Exercise the production clock-source decoder, monitor export and LED levels.
// Drive the split image's stored-index port and force existing media producers. No LED
// assignment, source decoder or monitor export is replaced by this fixture.
`default_nettype none
module led_datapath #(
  parameter int N_STREAMS_P = 1
) (
  input wire clk_i,
  input wire rst_ni,
  input wire [15:0] source_index_i,
  input wire [3:0] aaf_locked_i,
  input wire crf_locked_i,
  input wire [4:0] output_open_i,
  input wire clock_uncertain_i,
  input wire servo_locked_i,
  output wire [5:0] levels_o,
  output wire [3:0] monitor_locked_o,
  output wire stream_o,
  output wire clock_o
);
  milan_datapath #(.N_STREAMS(N_STREAMS_P), .GPTP_PLANE_EN_P(0), .CTRL_SPLIT_P(1)) dut (
    .axis_clk(clk_i), .axis_resetn(rst_ni),
    .i_ctl_clk_src_index(source_index_i),
    .o_led_input_locked(levels_o[0]), .o_led_output_open(levels_o[1]),
    .o_led_clock_internal(levels_o[2]), .o_led_clock_stream(levels_o[3]),
    .o_led_source_locked(levels_o[4]), .o_led_clock_locked(levels_o[5])
  );
  always_comb begin : drive_producers
    force dut.avtp_rx_monitor.locked_sh_r = aaf_locked_i[N_STREAMS_P-1:0];
    force dut.crf_locked_w = crf_locked_i;
    force dut.tkd_streaming_w = $bits(dut.tkd_streaming_w)'(output_open_i);
    force dut.clkv_tu_w = clock_uncertain_i;
    force dut.mcsrv_locked_w = servo_locked_i;
  end
  assign monitor_locked_o = 4'(dut.avtp_rx_monitor.media_locked_all_o);
  KL_status_led_truth truth (
    .clk_i, .rst_ni,
    .input_locked_i(levels_o[0]), .output_open_i(levels_o[1]),
    .clock_internal_i(levels_o[2]), .clock_stream_i(levels_o[3]),
    .source_locked_i(levels_o[4]), .clock_locked_i(levels_o[5]),
    .stream_o, .clock_o
  );
endmodule
`default_nettype wire
