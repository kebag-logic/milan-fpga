// SPDX-FileCopyrightText: 2026 Kebag Logic
// SPDX-License-Identifier: CERN-OHL-W-2.0
// The receiver samples the forwarded clock; input data arrives after its edge.
`timescale 1ns/1ps
module gpif_tb;
  logic clk=0, capture_clk=0, pin_clk=0, reset=1;
  always #10 clk=!clk;
  initial begin #12.083; forever #10 capture_clk=!capture_clk; end
  initial begin #11.042; forever #10 pin_clk=!pin_clk; end
  logic [15:0] dq_in=0;
  wire [15:0] dq_out, tristate_bus, rx_data;
  wire [1:0] address;
  wire wr_n, rd_n, oe_n, end_n, rx_valid, cap_ready, status_ready;
  logic flag=0, rx_ready=0, cap_valid=1, status_valid=0;
  wire [15:0] cap_data=16'(16'h4000+cap_sent);
  wire [15:0] status_data=16'(16'h9000+status_sent);
  wire cap_last=cap_sent%96==95, status_last=status_sent%10==9;
  int rx_sent=0,rx_seen=0,cap_sent=0,cap_seen=0,status_sent=0,status_seen=0;
  int cycles=0,address_age=0,last_status=0,status_records=0;
  int blocked_rx=0,blocked_capture=0;
  logic block_status=0;
  logic [1:0] previous_address=0;
  KL_usbaudio_gpif dut (
    .clk_i(clk),.capture_clk_i(capture_clk),.reset_i(reset),
    .dq_i(dq_in),.dq_o(dq_out),.dq_t_o(tristate_bus),.address_o(address),
    .slwr_n_o(wr_n),.slrd_n_o(rd_n),.sloe_n_o(oe_n),.pktend_n_o(end_n),.flaga_i(flag),
    .rx_valid_o(rx_valid),.rx_ready_i(rx_ready),.rx_data_o(rx_data),
    .capture_valid_i(cap_valid),.capture_ready_o(cap_ready),.capture_data_i(cap_data),
    .capture_last_i(cap_last),.capture_abort_i(1'b0),
    .status_valid_i(status_valid),.status_ready_o(status_ready),.status_data_i(status_data),
    .status_last_i(status_last)
  );
  always @(negedge clk) begin
    if(!reset) begin
      cycles=cycles+1;
      block_status=cycles>=60000 && cycles<120000;
      flag=address!=1 || !block_status;
      if(cycles==60000) begin blocked_rx=rx_seen;blocked_capture=cap_seen;end
      if(cycles==120000 && (rx_seen-blocked_rx<500 || cap_seen-blocked_capture<500))
        $fatal(1,"CHECK GPIF_BLOCKED_STATUS_FAIRNESS");
      rx_ready=cycles%23<18;
      if(cycles%25000==1) status_valid=1;
      if(address!=previous_address) address_age=0;
      else address_age=address_age+1;
      previous_address=address;
      if(cycles>51000 && (cycles<60000 || cycles>170000) && cycles-last_status>50000)
        $fatal(1,"CHECK STATUS_SERVICE_DEADLINE");
    end
  end
  always @(posedge clk) if(!reset) begin
    if(rx_valid && rx_ready) begin
      if(rx_data!=16'(16'h1000+rx_seen)) $fatal(1,"CHECK GPIF_READ_PIPELINE");
      rx_seen=rx_seen+1;
    end
    if(cap_ready) cap_sent=cap_sent+1;
    if(status_ready) begin
      if(status_last) status_valid<=0;
      status_sent<=status_sent+1;
    end
  end
  always @(posedge pin_clk) if(!reset) begin
    if(!wr_n && !rd_n) $fatal(1,"CHECK GPIF_TURNAROUND");
    if(!wr_n) begin
      if(tristate_bus!=0 || !oe_n || address_age<6) $fatal(1,"CHECK GPIF_WRITE_OWNERSHIP");
      if(address==0) begin
        if(dq_out!=16'(16'h4000+cap_seen)) $fatal(1,"CHECK GPIF_CAPTURE_BITS");
        if(!end_n != (cap_seen%96==95)) $fatal(1,"CHECK GPIF_CAPTURE_COMMIT");
        cap_seen=cap_seen+1;
      end else if(address==1) begin
        if(dq_out!=16'(16'h9000+status_seen)) $fatal(1,"CHECK GPIF_STATUS_BITS");
        if(!end_n != (status_seen%10==9)) $fatal(1,"CHECK GPIF_STATUS_COMMIT");
        status_seen=status_seen+1;
        if(!end_n) begin last_status=cycles;status_records=status_records+1;end
      end else $fatal(1,"CHECK GPIF_AUDIO_ADDRESSES");
    end
    if(!rd_n) begin
      if(address!=3 || tristate_bus!=16'hffff || oe_n || address_age<6)
        $fatal(1,"CHECK GPIF_READ_OWNERSHIP");
      dq_in<=#12.890 16'(16'h1000+rx_sent);
      rx_sent=rx_sent+1;
    end
    if(!end_n && wr_n) $fatal(1,"CHECK GPIF_END_WITH_WORD");
  end
  initial begin
    #100;reset=0;
    repeat(500000) @(negedge clk);
    if(rx_seen<10000 || cap_seen<10000 || status_records<16)
      $fatal(1,"CHECK GPIF_DUPLEX_SERVICE_COUNTS");
    if(rx_sent-rx_seen>1 || cap_seen-cap_sent>1 || status_seen-status_sent>1)
      $fatal(1,"CHECK GPIF_SINGLE_OUTSTANDING");
    // Reset inside an active write pulse: an already idle bus cannot prove
    // asynchronous pad shutdown, because a synchronous-only defect also idles.
    while(wr_n) @(negedge clk);
    #3;reset=1;#1;
    if(tristate_bus!=16'hffff || !wr_n || !rd_n || !oe_n || !end_n)
      $fatal(1,"CHECK GPIF_ASYNC_PAD_RESET");
    $display("PASS GPIF: %0d playback words, %0d capture words, %0d status records, phased sampling and reset",
             rx_seen,cap_seen,status_records);
    $finish;
  end
endmodule
