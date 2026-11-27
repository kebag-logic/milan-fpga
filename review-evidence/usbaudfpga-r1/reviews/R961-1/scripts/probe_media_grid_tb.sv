// Reviewer probe: does every media grid event produce exactly one whole-frame
// walk into the capture mapper (four pairs and one capture_tick) when a
// playback state change is applied on the grid cycle or during the walk?
`timescale 1ns/1ps
module probe_media_grid_tb;
  logic clk = 0;
  always #5 clk = !clk;
  logic rst_n = 0, tick = 0, state_valid = 0, play_valid = 0;
  logic [66:0] state_data = 0;
  logic [287:0] play_data = 0;
  logic [6:0] level = 0;
  wire state_ready, ack_valid, play_ready, pair_valid, capture_tick, capture_valid, error_value;
  wire [31:0] ack_epoch, left_value, right_value, frame_ns, gaps, drops, frames;
  wire [3:0] pair_slot;
  wire [287:0] capture_data;
  wire [1:0] running;
  wire [13:0] extremes;
  int ticks = 0, snapshots = 0, pairs = 0;
  KL_usbaudio_media dut (
    .clk_i(clk), .rst_n(rst_n), .media_tick_i(tick), .media_ns_i(32'd0),
    .state_valid_i(state_valid), .state_ready_o(state_ready), .state_i(state_data),
    .ack_valid_o(ack_valid), .ack_ready_i(1'b1), .ack_epoch_o(ack_epoch),
    .playback_valid_i(play_valid), .playback_ready_o(play_ready), .playback_i(play_data),
    .playback_level_i(level), .pair_valid_o(pair_valid), .pair_slot_o(pair_slot),
    .pair_l_o(left_value), .pair_r_o(right_value), .frame_ns_o(frame_ns),
    .capture_tick_o(capture_tick), .render_data_i(64'd0), .render_valid_i(1'b0),
    .render_last_i(1'b0), .render_stream_i(4'd0), .render_tick_i(1'b0),
    .capture_valid_o(capture_valid), .capture_ready_i(1'b1), .capture_o(capture_data),
    .gaps_o(gaps), .drops_o(drops), .frames_o(frames), .running_o(running),
    .playback_extremes_o(extremes), .error_o(error_value));
  always @(posedge clk) if (rst_n) begin
    if (tick) ticks++;
    if (capture_tick) snapshots++;
    if (pair_valid) pairs++;
  end
  task automatic step(input int n = 1);
    repeat (n) begin @(posedge clk); #1; end
  endtask
  // One grid event every 40 cycles; optionally present a playback epoch
  // change at offset `at` cycles after the grid cycle (0 = same cycle).
  task automatic grid_with_change(input int at, input int epoch);
    for (int c = 0; c < 40; c++) begin
      tick = (c == 0);
      if (at >= 0 && c == at) begin state_data = {32'd1, 32'(epoch), 3'd7}; state_valid = 1; end
      else state_valid = 0;
      step();
    end
    tick = 0; state_valid = 0;
  endtask
  initial begin
    int case_ticks, case_snaps;
    step(4); rst_n = 1; step(4);
    state_data = {32'd1, 32'd1, 3'd7}; state_valid = 1; step(); state_valid = 0; step(4);
    for (int g = 0; g < 4; g++) grid_with_change(-1, 0);
    $display("PROBE baseline: ticks=%0d snapshots=%0d pairs=%0d", ticks, snapshots, pairs);
    for (int at = 0; at < 8; at++) begin
      case_ticks = ticks; case_snaps = snapshots;
      grid_with_change(at, 2 + at);
      grid_with_change(-1, 0);
      $display("PROBE playback epoch change %0d cycles after the grid cycle: grid events=%0d snapshots=%0d",
               at, ticks - case_ticks, snapshots - case_snaps);
    end
    $display("PROBE total: ticks=%0d snapshots=%0d pairs=%0d gaps=%0d error=%0d",
             ticks, snapshots, pairs, gaps, error_value);
    if (snapshots != ticks) $display("PROBE RESULT: MISSING_GRID_SNAPSHOT %0d", ticks - snapshots);
    else $display("PROBE RESULT: EVERY_GRID_SNAPSHOT");
    $finish;
  end
endmodule
