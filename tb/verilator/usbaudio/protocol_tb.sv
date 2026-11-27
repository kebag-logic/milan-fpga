// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// Independent byte-level checks of the three protocol leaves, not the bridge.
`timescale 1ns/1ps
module protocol_tb;
  logic clk;
  initial begin
    clk = 0;
    forever #5 clk = !clk;
  end
  logic rst_n = 0;
  logic in_valid = 0, record_ready = 0;
  logic [15:0] in_data = 0;
  wire in_ready, record_valid, record_done;
  wire [31:0] playback_epoch, capture_epoch, rejected, digest_errors;
  wire [2:0] flags, frames;
  wire [1791:0] pcm;
  KL_usbaudio_record record_dut (
    .clk_i(clk), .rst_n(rst_n), .valid_i(in_valid), .ready_o(in_ready),
    .data_i(in_data), .record_valid_o(record_valid), .record_ready_i(record_ready),
    .playback_epoch_o(playback_epoch), .capture_epoch_o(capture_epoch),
    .flags_o(flags), .frames_o(frames), .pcm_o(pcm),
    .rejected_o(rejected), .digest_errors_o(digest_errors), .done_o(record_done));
  always @(posedge clk) if (rst_n && record_done && !(in_valid && in_ready))
    $fatal(1, "CHECK RECORD_DONE_TRANSFER");
  logic snapshot_valid = 0, status_ready = 0;
  logic [31:0] status_feedback = 0, status_rate = 0, status_epoch = 0;
  logic [3:0] status_flags = 0;
  wire snapshot_ready, status_valid, status_last;
  wire [15:0] status_data;
  KL_usbaudio_status status_dut (
    .clk_i(clk), .rst_n(rst_n), .snapshot_valid_i(snapshot_valid),
    .snapshot_ready_o(snapshot_ready), .feedback_samples_q16_i(status_feedback),
    .rate_hz_i(status_rate), .flags_i(status_flags), .capture_epoch_i(status_epoch),
    .valid_o(status_valid), .ready_i(status_ready), .data_o(status_data),
    .last_o(status_last));
  logic locked = 0, interval = 0;
  logic [31:0] events = 0;
  wire [31:0] feedback;
  wire measured;
  KL_usbaudio_feedback feedback_dut (
    .clk_i(clk), .rst_n(rst_n), .locked_i(locked), .interval_i(interval),
    .media_events_i(events), .feedback_samples_q16_o(feedback), .measured_o(measured));

  task automatic step;
    @(posedge clk); #1;
    @(negedge clk); #1;
  endtask
  task automatic check(input bit ok, input string name);
    if (!ok) $fatal(1, "CHECK %s", name);
  endtask
  task automatic reset_all;
    rst_n = 0; in_valid = 0; record_ready = 0;
    snapshot_valid = 0; status_ready = 0; interval = 0;
    step(); step(); rst_n = 1; step();
    check(in_ready && !record_valid && !status_valid && !measured, "RESET");
  endtask
  function automatic logic [31:0] sample(input int unsigned index);
    // All bits vary, including the low byte that the media queue currently loses.
    return (index * 32'h9e3779b9) ^ 32'hca5a00ff;
  endfunction
  task automatic send_word(input logic [15:0] word_value, input bit stall);
    in_valid = 0;
    if (stall) begin
      step(); check(!record_valid, "PARTIAL_NOT_VISIBLE");
    end
    check(in_ready && !record_valid, "RECORD_INPUT_READY");
    in_data = word_value; in_valid = 1; step(); in_valid = 0;
  endtask
  task automatic send_record(input int unsigned length_bytes,
                             input logic [31:0] play, cap,
                             input logic [15:0] flag_value, magic, digest,
                             input int unsigned first_sample);
    send_word(magic, 1);
    send_word(16'(length_bytes), 0);
    send_word(play[15:0], 1); send_word(play[31:16], 0);
    send_word(cap[15:0], 0); send_word(cap[31:16], 1);
    send_word(flag_value, 0); send_word(digest, 0);
    for (int unsigned w = 0; w < (length_bytes + 1)/2; w++)
      send_word(16'(sample(first_sample + w/2) >> (16*(w%2))), w%19 == 0);
  endtask
  task automatic take_record(input int unsigned frame_count,
                             input logic [31:0] play, cap,
                             input logic [2:0] flag_value,
                             input int unsigned first_sample);
    logic [1791:0] hold_value;
    check(record_valid && !in_ready, "COMPLETE_RECORD");
    check(frames == 3'(frame_count), "FRAME_COUNT");
    check(playback_epoch == play && capture_epoch == cap, "INDEPENDENT_EPOCHS");
    check(flags == flag_value, "FLAGS");
    for (int unsigned s = 0; s < frame_count*8; s++)
      check(pcm[s*32 +: 32] == sample(first_sample+s), "PCM_ALL_BITS_ORDER");
    hold_value = pcm;
    in_valid = 1; in_data = '1;
    repeat (3) begin
      step(); check(record_valid && !in_ready && pcm == hold_value, "RECORD_BACKPRESSURE");
      check(playback_epoch == play && capture_epoch == cap, "EPOCH_BACKPRESSURE");
    end
    in_valid = 0; record_ready = 1; step(); record_ready = 0;
    check(!record_valid && in_ready, "CONSUMED_ONCE");
  endtask

  task automatic test_records;
    int unsigned first_sample, frame_count, nreject, ndigest;
    logic [31:0] cap, play;
    reset_all();
    first_sample = 0;
    for (int unsigned n = 0; n < 120000; n++) begin
      frame_count = 1 + n%7;
      play = n < 60000 ? 32'hfffffffe : 32'h00000003;
      cap = 32'hffff0000 + n/11;
      send_record(frame_count*32, play, cap, 7, 'h554f, 'h84ff, first_sample);
      take_record(frame_count, play, cap, 7, first_sample);
      first_sample += frame_count*8;
    end
    // Every state combination remains readable, including playback inactive.
    for (int unsigned f = 0; f < 8; f++) begin
      send_record(0, 32'hffffffff-f, 32'h00010000+f, 16'(f), 'h554f, 'h84ff, 0);
      take_record(0, 32'hffffffff-f, 32'h00010000+f, 3'(f), 0);
    end
    nreject = 0; ndigest = 0;
    for (int unsigned n = 0; n < 10; n++) begin
      case (n)
        0: send_record(32, 1, 2, 7, 'h554e, 'h84ff, 0);
        1: send_record(32, 1, 2, 7, 'h554f, 'h84fe, 0);
        2: send_record(31, 1, 2, 7, 'h554f, 'h84ff, 0);
        3: send_record(256, 1, 2, 7, 'h554f, 'h84ff, 0);
        4: send_record(32, 1, 2, 15, 'h554f, 'h84ff, 0);
        5: send_record(32, 1, 2, 1, 'h554f, 'h84ff, 0);
        6: send_record(32, 1, 2, 2, 'h554f, 'h84ff, 0);
        7: send_record(65535, 1, 2, 7, 'h554f, 'h84ff, 0);
        8: send_record(0, 1, 2, 7, 'h554f, 'h8400, 0);
        9: send_record(30, 1, 2, 7, 'h554f, 'h84ff, 0);
        default: $fatal;
      endcase
      nreject++; if (n == 1 || n == 8) ndigest++;
      check(!record_valid && rejected == nreject, "BAD_RECORD_DRAIN");
      check(digest_errors == ndigest, "DIGEST_COUNT");
      send_record(32, 2, 3, 3, 'h554f, 'h84ff, n);
      take_record(1, 2, 3, 3, n);
    end
    // Every word boundary of a maximal record can be a hard session boundary.
    for (int unsigned cut = 0; cut < 120; cut++) begin
      reset_all();
      for (int unsigned w = 0; w < cut; w++) begin
        case (w)
          0: send_word('h554f, 0);
          1: send_word(224, 0);
          6: send_word(7, 0);
          7: send_word('h84ff, 0);
          default: send_word(16'(w), 0);
        endcase
      end
      reset_all(); send_record(32, 1, 1, 3, 'h554f, 'h84ff, cut);
      take_record(1, 1, 1, 3, cut);
    end
    $display("PASS record stream: 120000 records, %0d samples, all bits and order", first_sample);
  endtask

  task automatic test_status;
    logic [159:0] expected;
    reset_all();
    for (int unsigned n = 0; n < 65539; n++) begin
      status_feedback = 32'h60000 + n;
      status_rate = n%2 == 0 ? 48000 : 96000;
      status_flags = 4'(n);
      status_epoch = 32'hffff8000 + n;
      expected = {status_epoch, 16'h84ff, 12'b0, status_flags,
                  status_rate, status_feedback, 16'(n), 16'h5541};
      check(snapshot_ready, "STATUS_READY");
      snapshot_valid = 1; step();
      // Simultaneous new snapshots must never corrupt an in-flight record.
      status_feedback = ~status_feedback; status_epoch = ~status_epoch;
      status_rate = ~status_rate; status_flags = ~status_flags;
      for (int unsigned w = 0; w < 10; w++) begin
        status_ready = 0; step();
        check(status_valid && !snapshot_ready, "STATUS_BACKPRESSURE");
        check(status_data == expected[w*16 +: 16], "STATUS_BYTES");
        check(status_last == (w == 9), "STATUS_LENGTH");
        status_ready = 1; step();
      end
      status_ready = 0; snapshot_valid = 0;
      check(!status_valid && snapshot_ready, "STATUS_COMMIT");
    end
    for (int unsigned cut = 0; cut < 10; cut++) begin
      snapshot_valid = 1; step(); snapshot_valid = 0; status_ready = 1;
      repeat (cut) step();
      reset_all();
    end
    $display("PASS status: 65539 exact 20-byte records, sequence wrap, stalls and reset");
  endtask

  task automatic tick_interval(input int unsigned count);
    events = count; interval = 1; step(); interval = 0;
    // Independent intervals, deliberately irregular in local clock cycles.
    repeat (2 + count%3) step();
  endtask
  task automatic test_feedback;
    int unsigned cumulative;
    reset_all();
    check(feedback == 0, "FEEDBACK_UNLOCKED");
    locked = 1; step();
    check(feedback == 0 && !measured, "FEEDBACK_STARTUP");
    cumulative = 32'hffff8000;
    tick_interval(cumulative);
    for (int unsigned window = 0; window < 3; window++) begin
      for (int unsigned i = 0; i < 8192; i++) begin
        cumulative += 6 + ((window == 1 && i == 77) ? 1 : 0);
        tick_interval(cumulative);
        if (window == 0 && i < 8191) check(!measured, "FEEDBACK_WINDOW_LENGTH");
      end
      check(measured, "FEEDBACK_MEASURED");
      check(feedback == (window == 1 ? 'h60008 : 'h60000), "FEEDBACK_VALUE");
    end
    repeat (10000) begin events++; step(); end
    check(feedback == 'h60000, "NO_LOCAL_CLOCK_REFERENCE");
    locked = 0; step();
    check(!measured && feedback == 0, "FEEDBACK_LOCK_LOSS");
    locked = 1; step();
    check(!measured && feedback == 0, "FEEDBACK_RELOCK");
    $display("PASS feedback: 49152 and 49153 events, counter wrap, lock and reference gating");
  endtask
  initial begin
    string selected;
    if (!$value$plusargs("case=%s", selected)) selected = "all";
    if (selected == "all" || selected == "record") test_records();
    if (selected == "all" || selected == "status") test_status();
    if (selected == "all" || selected == "feedback") test_feedback();
    $display("PASS protocol leaves; integrated transport not exercised");
    $finish;
  end
endmodule
