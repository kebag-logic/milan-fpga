// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
`timescale 1ns/1ps
module reference_tb;
  logic clk = 0;
  // Match the watchdog's independent 100 kHz time base exactly.
  always #5000 clk = !clk;
  logic rst_n = 0, valid = 0;
  logic [15:0] data = 0;
  logic [47:0] media_ticks = 0;
  wire ready, reference_p, loss_p, discontinuity, record_valid;
  wire [13:0] count;
  wire [31:0] sequence_value, feedback, losses;
  wire [12:0] delta;
  wire [47:0] stamp;
  wire locked, accepted;
  time last_reference_time;
  bit last_reference_accepted;
  logic media_locked = 1, physical = 1;
  int unsigned sequence_sent;
  int unsigned count_sent;
  logic [47:0] ticks_sent;
  int unsigned references_seen = 0, malformed_seen = 0;
  logic [159:0] words;
  KL_usbaudio_ingress ingress (
    .clk_i(clk), .rst_n(rst_n), .valid_i(valid), .ready_o(ready), .data_i(data),
    .media_ticks_i(media_ticks), .record_valid_o(record_valid), .record_ready_i(1'b1),
    .playback_epoch_o(), .capture_epoch_o(), .flags_o(), .frames_o(), .pcm_o(),
    .reference_p_o(reference_p), .loss_p_o(loss_p), .count_o(count),
    .sequence_o(sequence_value), .delta_usb_cycles_o(delta), .discontinuity_o(discontinuity),
    .stamp_ticks_o(stamp), .rejected_o(), .digest_errors_o()
  );
  KL_usbaudio_reference #(.BUS_HZ_P(100000)) estimator (
    .clk_i(clk), .rst_n(rst_n), .media_locked_i(media_locked), .latency_qualified_i(physical),
    .reference_i(reference_p), .malformed_i(loss_p), .count_i(count),
    .sequence_i(sequence_value), .delta_usb_cycles_i(delta), .discontinuity_i(discontinuity),
    .stamp_ticks_i(stamp), .locked_o(locked), .feedback_samples_q16_o(feedback), .losses_o(losses),
    .accepted_o(accepted)
  );
  always @(posedge clk) begin
    if (rst_n && reference_p) begin
      last_reference_time = $time;
      last_reference_accepted = accepted;
    end
  end
  always @(negedge clk) begin
    if (reference_p) references_seen++;
    if (loss_p) malformed_seen++;
  end
  task automatic check(input bit condition, input string label_value);
    if (!condition) $fatal(1, "CHECK %s", label_value);
  endtask
  task automatic step;
    @(posedge clk); #1;
  endtask
  task automatic reset_all;
    rst_n = 0; valid = 0; media_locked = 1; physical = 1;
    repeat (4) step(); rst_n = 1; step();
    sequence_sent = 32'hfffffffa;
    count_sent = 16336;
    ticks_sent = 48'h0fffffff0000;
  endtask
  task automatic word_send(input logic [15:0] value);
    data = value; valid = 1;
    check(ready, "REFERENCE_DRAIN"); step(); valid = 0; step();
  endtask
  task automatic send_reference(input int field = -1, input int bit_index = 0,
                                input int raw_delta = 0, input int tick_extra = 0,
                                input int trailing_cycles = 78);
    int before_count;
    logic [47:0] first_stamp;
    sequence_sent++;
    count_sent = (count_sent+8)&16383;
    ticks_sent += 48'(24576+tick_extra);
    first_stamp = ticks_sent;
    words = {16'h84ff, 16'd0, 5'd0, 13'(raw_delta), 14'(count_sent),
             32'(sequence_sent), 16'(count_sent), 16'h0801, 16'd20, 16'h5549};
    if (field >= 0) words[field*16+bit_index] = ~words[field*16+bit_index];
    // Misalignment must be tested with a coherent raw count, or the separate
    // raw/count equality check would mask a missing alignment check.
    if (field == 3 && bit_index == 0) words[96] = ~words[96];
    before_count = references_seen;
    for (int index = 0; index < 10; index++) begin
      media_ticks = index == 0 ? first_stamp : first_stamp+48'(index*997);
      word_send(words[index*16 +: 16]);
    end
    step();
    if (references_seen != before_count) begin
      check(stamp == first_stamp, "REFERENCE_FIRST_WORD_TIMESTAMP");
      check(!record_valid, "REFERENCE_NOT_PCM");
    end
    repeat (trailing_cycles) step();
  endtask
  task automatic wait_reference_age(input int cycles);
    while (($time-last_reference_time)/10000 < 64'(cycles)) step();
    check(($time-last_reference_time)/10000 == 64'(cycles), "REFERENCE_WATCHDOG_TEST_AGE");
  endtask
  task automatic watchdog_bounds;
    time previous_time;
    logic [31:0] previous_losses;
    reset_all(); qualify();
    previous_time = last_reference_time;
    previous_losses = losses;
    // The ten-word parser needs twenty edges through reference consumption.
    // Keep the source-clock timestamps continuous to isolate the own-clock
    // watchdog from the independent late/bunched-delivery checks.
    wait_reference_age(270);
    send_reference(-1, 0, 0, 0, 0);
    check(last_reference_time-previous_time == 2900000, "REFERENCE_WATCHDOG_2P9MS_AGE");
    check(last_reference_accepted && locked && feedback == 32'h60000
          && losses == previous_losses, "REFERENCE_WATCHDOG_2P9MS_ACCEPTED");
    previous_time = last_reference_time;
    wait_reference_age(280);
    send_reference(-1, 0, 0, 0, 0);
    check(last_reference_time-previous_time == 3000000, "REFERENCE_WATCHDOG_3MS_AGE");
    check(!last_reference_accepted && !locked && feedback == 0
          && losses == previous_losses+1, "REFERENCE_WATCHDOG_3MS_REFUSED");
    // The refused record cannot seed the replacement measurement window.
    qualify();
    previous_losses = losses;
    // No new record, and no advancing media timestamp: our clock must expire.
    wait_reference_age(299);
    check(locked && feedback == 32'h60000, "REFERENCE_WATCHDOG_BEFORE_3MS");
    step();
    check(!locked && feedback == 0 && losses == previous_losses+1,
          "REFERENCE_WATCHDOG_3MS_NO_REFERENCE");
    $display("PASS reference watchdog: 2.9 ms accepted; 3 ms replacement refused; own-clock expiry without references");
  endtask
  task automatic qualify;
    for (int n = 0; n < 1025; n++) begin
      send_reference();
      if (n < 1024) check(!locked, "SELECTED_REFERENCE_WINDOW");
    end
    check(locked && feedback == 32'h60000, "SELECTED_REFERENCE_RATE");
  endtask
  initial begin
    int previous;
    string selected;
    if (!$value$plusargs("case=%s", selected)) selected = "all";
    if (selected == "all" || selected == "fields") begin
      // Every field is damaged independently, including each reserved region.
      for (int row = 0; row < 10; row++) begin
        reset_all(); qualify(); previous = malformed_seen;
        case (row)
          0: send_reference(0, 1);
          1: send_reference(1, 0);
          2: send_reference(2, 0);
          3: send_reference(2, 8);
          4: send_reference(3, 14);
          5: send_reference(3, 0);
          6: send_reference(6, 0);
          7: send_reference(7, 11);
          8: send_reference(8, 1);
          9: send_reference(9, 0);
        endcase
        check(!locked && feedback == 0 && malformed_seen > previous, "REFERENCE_FIELDS_REJECTED");
      end
      $display("PASS reference structure: magic, length, version, period, count, raw, flags and digest");
    end
    if (selected == "all" || selected == "continuity") begin
      reset_all(); qualify();
      send_reference(4, 1); check(!locked && feedback == 0, "REFERENCE_SEQUENCE_GAP");
      reset_all(); qualify(); sequence_sent--;
      send_reference(); check(!locked, "REFERENCE_SEQUENCE_DUPLICATE");
      reset_all(); qualify(); count_sent += 8;
      send_reference(); check(!locked, "REFERENCE_COUNT_GAP");
      reset_all(); qualify(); send_reference(8, 0);
      check(!locked, "REFERENCE_DISCONTINUITY");
      reset_all(); qualify(); send_reference(-1, 0, 7500);
      check(!locked, "REFERENCE_DELTA_RANGE");
      watchdog_bounds();
      reset_all(); qualify(); send_reference(-1, 0, 0, -20000);
      check(!locked, "REFERENCE_BUNCHED");
      reset_all(); qualify(); send_reference(-1, 0, 0, 20000);
      check(!locked, "REFERENCE_LATE");
      reset_all(); qualify(); physical = 0; step();
      check(!locked && feedback == 0, "REFERENCE_PHYSICAL_BOUND");
      physical = 1; media_locked = 0; step();
      check(!locked && feedback == 0, "REFERENCE_MEDIA_LOSS");
      $display("PASS reference continuity: wraps, gaps, duplicates, loss, watchdog, delivery bounds and clock loss");
    end
    if (selected == "all" || selected == "delta") begin
      reset_all();
      // Place the baseline 400 ticks after a media frame, then delay each
      // following ITP by 625 USB units = exactly 256 media ticks.
      ticks_sent = 48'd400;
      send_reference();
      for (int n = 0; n < 1024; n++) send_reference(-1, 0, 625, n == 0 ? 256 : 0);
      check(locked && feedback == 32'h60000, "REFERENCE_DELTA_UNITS");
      reset_all();
      send_reference();
      for (int n = 0; n < 1024; n++) send_reference(-1, 0, 0, n == 77 ? 512 : 0);
      check(locked && feedback == 32'h60008, "REFERENCE_EXTRA_EVENT");
      $display("PASS ITP delta: 1/60 MHz units and extra media event");
    end
    $finish;
  end
endmodule
