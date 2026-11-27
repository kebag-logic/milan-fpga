// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
`timescale 1ns/1ps
module packet_tb;
  logic clk=0;
  always #5 clk=!clk;
  logic rst_n=0, reference_p=0, enabled=0, fence=0, frame_valid=0, ready=0;
  logic [31:0] epoch=1;
  logic [287:0] frame_data=0;
  logic [6:0] level=0;
  wire frame_ready, valid, last;
  wire [15:0] data;
  wire [31:0] gaps, abandoned;
  int source_frame=0, sent_words=0, packets=0;
  logic auto_source=0, score=0;
  int expected_first=0;
  KL_usbaudio_packet #(.BUS_HZ_P(800000)) dut (
    .clk_i(clk), .rst_n(rst_n), .reference_i(reference_p), .enabled_i(enabled),
    .fence_i(fence), .epoch_i(epoch), .frame_valid_i(frame_valid), .frame_ready_o(frame_ready),
    .frame_i(frame_data), .level_i(level), .valid_o(valid), .ready_i(ready),
    .data_o(data), .last_o(last), .gaps_o(gaps), .abandoned_o(abandoned)
  );
  function automatic logic [15:0] word_value(input int frame, input int word_index);
    return 16'(frame*193+word_index*17+1);
  endfunction
  always_comb begin
    frame_data[287:256]=epoch;
    for (int w=0;w<16;w++) frame_data[w*16+:16]=word_value(source_frame,w);
  end
  always @(posedge clk) begin
    if (rst_n && auto_source && frame_valid && frame_ready) source_frame<=source_frame+1;
    if (rst_n && score && valid && ready) begin
      if (data != word_value(expected_first+sent_words/16,sent_words%16))
        $fatal(1,"CHECK PACKET_BITS_ORDER");
      sent_words=sent_words+1;
      if (last) begin
        if (sent_words%16 != 0 || sent_words>112) $fatal(1,"CHECK PACKET_WHOLE_FRAME");
        packets=packets+1;
      end
    end
  end
  task automatic step(input int n=1);
    repeat(n) begin @(posedge clk); #1; @(negedge clk); #1; end
  endtask
  task automatic check(input bit condition,input string name);
    if(!condition) $fatal(1,"CHECK %s",name);
  endtask
  task automatic wait_word;
    int budget;
    budget=300;
    while(!valid && budget>0) begin step(); budget--; end
    check(valid,"PACKET_AVAILABLE");
  endtask
  initial begin
    logic [15:0] held;
    step(4); rst_n=1;step(4);
    reference_p=1;step();reference_p=0;step(799);reference_p=1;step();reference_p=0;
    enabled=1;level=11;frame_valid=1;auto_source=1;
    step(110); check(!valid && !frame_ready && gaps==0,"PACKET_PREFILL");
    level=12;wait_word();level=0;
    // Every stalled word is retained, including a deliberately stalled last word.
    score=1;ready=1;step(13);ready=0;held=data;step(250);
    check(valid && data==held && !last,"PACKET_STALL_POSITION");
    ready=1;step(98);ready=0;
    check(valid && last,"PACKET_LAST_BOUNDARY");held=data;step(9);
    check(valid && last && data==held,"PACKET_LAST_STALL");
    ready=1;step();ready=0;
    check(packets==1 && sent_words==112,"PACKET_COMMIT_ONCE");
    check(gaps!=0,"PACKET_MISSED_SERVICE_COUNTED");
    // An epoch discards the current partial interval; normal backpressure did not.
    level=6;sent_words=0;expected_first=source_frame;wait_word();ready=1;step(7);ready=0;
    fence=1;step();fence=0;epoch=2;score=0;
    check(!valid && abandoned==6,"PACKET_EPOCH_ABANDON");
    level=11;step(110);check(!valid,"PACKET_EPOCH_REPREFILL");
    expected_first=source_frame;sent_words=0;level=12;wait_word();level=0;score=1;ready=1;step(112);ready=0;
    check(packets==2 && sent_words==112,"PACKET_EPOCH_CHANNEL_ZERO");
    // A session reset also cancels an incomplete word stream immediately.
    level=6;score=0;wait_word();ready=1;step(3);ready=0;rst_n=0;step();
    check(!valid && gaps==0 && abandoned==0,"PACKET_RESET");
    $display("PASS capture packets: prefill, all bits, stalls, commit, service loss, epoch fence and reset");
    $finish;
  end
endmodule
