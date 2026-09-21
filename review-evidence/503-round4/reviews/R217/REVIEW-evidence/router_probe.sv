`timescale 1ns/1ps
module router_probe #(parameter int MODE = 0);
  logic clk=0, rst_n=0, walk_done=0, lready=0;
  logic [1:0] strobes=0;
  logic [1:0][15:0] payloads=0;
  wire rv, rs, lost, rawlv, rawpr, own, released;
  wire [15:0] rp;
  wire [7:0] count;
  wire lv = (MODE == 1) ? rv : rawlv;
  wire pr = (MODE == 2) ? lready : rawpr;
  int takes=0, pops=0;
  logic [15:0] got[3];
  KL_pp_event_router #(.N_SRC_P(2), .PAYLOAD_W_P(16)) router (
    .clk_i(clk), .rst_n(rst_n), .src_strobe_i(strobes), .src_payload_i(payloads),
    .evt_valid_o(rv), .evt_src_o(rs), .evt_payload_o(rp), .evt_lost_o(lost),
    .evt_ack_i(pr), .lost_src_i(1'b0), .lost_count_o(count));
  KL_pp_acmp_lsn_admit #(.N_SINKS_P(9)) gate0 (
    .clk_i(clk), .rst_n(rst_n), .walk_done_i(walk_done), .pre_valid_i(1'b0),
    .lsn_busy_i(1'b0), .lsn_arm_i(1'b0), .own_o(own), .released_o(released),
    .p_txn_valid_i(1'b0), .p_txn_ready_o(), .l_txn_valid_o(), .l_txn_ready_i(1'b1),
    .p_tk_valid_i(rv), .p_tk_ready_o(rawpr), .l_tk_valid_o(rawlv), .l_tk_ready_i(lready),
    .p_strm_valid_i(1'b0), .l_strm_valid_o(), .p_exp_valid_i(1'b0),
    .p_exp_owner_i(8'd32), .l_exp_valid_o(), .dbg_exp_drop_o());
  always @(posedge clk) if (rst_n) begin
    if ((lv && lready) != (rv && pr)) $fatal(1,"pop/take disagreement MODE=%0d",MODE);
    if (own && ((lv && lready) || (rv && pr))) $fatal(1,"consumed while owned MODE=%0d",MODE);
    if (lv && lready) begin
      if (takes >= 3) $fatal(1,"duplicate delivery");
      got[takes] = rp;
      takes++;
    end
    if (rv && pr) pops++;
  end
  task step; #5; clk=1; #5; clk=0; endtask
  initial begin
    step(); rst_n=1; lready=1;
    payloads[0]=16'h0101; strobes=1; step(); strobes=0; step();
    if (!rv || rp!=16'h0101 || !own) $fatal(1,"held first event missing");
    repeat(3) step();
    payloads[0]=16'hffff; payloads[1]=16'h0202; strobes=3; step(); strobes=0;
    repeat(3) step();
    if (rp!=16'h0101 || count!=1 || !lost || takes!=0 || pops!=0)
      $fatal(1,"coalescing changed held payload or consumed an event");
    lready=0; walk_done=1; step();
    if (!released || own) $fatal(1,"not released");
    repeat(3) step();
    if (takes!=0 || pops!=0 || rp!=16'h0101) $fatal(1,"backpressure did not hold");
    // Re-fire the acknowledged source on its delivery edge: a new event.
    lready=1; payloads[0]=16'h0303; strobes=1; step(); strobes=0;
    repeat(5) step();
    if (takes!=3 || pops!=3 || got[0]!=16'h0101 || got[1]!=16'h0202 || got[2]!=16'h0303 || count!=1)
      $fatal(1,"wrong deliveries or ack-edge coalescing");
    rst_n=0; step(); rst_n=1; walk_done=0; step();
    if (!own || rv || count!=0) $fatal(1,"reset did not re-own and clear");
    $display("PASS real router + S4: held first payload, coalescing count, two sources, release backpressure, ack-edge refire, reset; takes=%0d pops=%0d",takes,pops);
    $finish;
  end
endmodule
