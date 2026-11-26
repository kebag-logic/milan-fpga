// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Inject decoded-level hazards between source edges across a destination edge.
`timescale 1ns/1ps
module levels_tb;
  logic bus_clk=0, media_clk=0, reset=1, media_locked=0, check_quiet=0;
  always #10 bus_clk=!bus_clk;
  always #13 media_clk=!media_clk;
  KL_usbaudio_bridge dut (
    .bus_clk_i(bus_clk),.media_clk_i(media_clk),.oscillator_clk_i(1'b0),
    .reset_i(reset),.media_locked_i(media_locked),.latency_qualified_i(1'b0),
    .rx_valid_i(1'b0),.rx_ready_o(),.rx_data_i(16'd0),
    .capture_valid_o(),.capture_ready_i(1'b1),.capture_data_o(),
    .capture_last_o(),.capture_abort_o(),.status_valid_o(),.status_ready_i(1'b1),
    .status_data_o(),.status_last_o(),.media_tick_i(1'b0),.media_ns_i(32'd0),
    .render_data_i(64'd0),.render_valid_i(1'b0),.render_last_i(1'b0),
    .render_stream_i(4'd0),.render_tick_i(1'b0),.pair_valid_o(),.pair_slot_o(),
    .pair_l_o(),.pair_r_o(),.frame_ns_o(),.capture_tick_o(),.locked_o(),
    .feedback_q16_o(),.error_o(),.playback_drops_o(),.playback_gaps_o(),
    .capture_drops_o(),.reference_losses_o(),.rejected_records_o(),
    .digest_errors_o(),.media_frames_o(),.playback_extremes_o(),.capture_extremes_o()
  );
  // These are the actual receiving synchronizers. Observing every bus edge
  // prevents a brief error from hiding between periodic status snapshots.
  always @(negedge bus_clk) if(check_quiet) begin
    if(!dut.lock_r[1]) $fatal(1,"CHECK LEVEL_CLOCK_GLITCH");
    if(dut.running_sync_r[1]) $fatal(1,"CHECK LEVEL_PLAYBACK_GLITCH");
    if(dut.running_sync_r[0]) $fatal(1,"CHECK LEVEL_CAPTURE_GLITCH");
  end
  initial begin
    force dut.media_running_w=2'b00;
    #100;reset=0;media_locked=1;
    repeat(10) @(negedge bus_clk);
    if(!dut.lock_r[1] || dut.running_sync_r!=0) $fatal(1,"CHECK LEVEL_INITIAL_STATE");
    check_quiet=1;
    repeat(50) begin
      // A two-nanosecond decode pulse straddles a receiving edge but no
      // source rising edge. The clocks deliberately have different periods.
      do @(negedge bus_clk);
      while((($time+23)%26)<=2 || (($time+23)%26)>=24);
      #9;media_locked=0;force dut.media_running_w=2'b11;
      #2;media_locked=1;force dut.media_running_w=2'b00;
      repeat(4) @(negedge bus_clk);
    end
    check_quiet=0;
    media_locked=0;force dut.media_running_w=2'b11;
    repeat(10) @(negedge bus_clk);
    if(dut.lock_r[1] || dut.running_sync_r!=3) $fatal(1,"CHECK LEVEL_STABLE_TRANSITION");
    media_locked=1;force dut.media_running_w=2'b00;
    repeat(10) @(negedge bus_clk);
    if(!dut.lock_r[1] || dut.running_sync_r!=0) $fatal(1,"CHECK LEVEL_RETURN_TRANSITION");
    reset=1;
    repeat(10) @(negedge bus_clk);
    if(dut.lock_r!=0 || dut.running_sync_r!=0) $fatal(1,"CHECK LEVEL_RESET");
    $display("PASS source levels: 50 hazards, stable transitions and reset on actual bridge crossings");
    $finish;
  end
endmodule
