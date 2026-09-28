// Reviewer probe R395-1: the latest strobe offset (cycles after the tick
// cycle) at which pair p's new value still reaches the walk that tick starts,
// per pair, for whichever KL_chan_map_capture is compiled (base or head; the
// head gets its default TDM_FRAME_PAIRS_P = 4). Head: pair p's own strobe
// never publishes unless p = 3, so for the head the pair-3 (close) offset is
// the one that matters; pairs 0..2 are measured with the whole rest of the
// frame already staged and pair 3 strobed in the same cycle as pair p.
`default_nettype none
module tb_read;
  logic clk = 0;
  always #5 clk = ~clk;
  logic rst_n = 0, pv = 0, tick = 0, mwe = 0;
  logic [3:0] slot = 0;
  logic [23:0] l = 0, r = 0;
  logic [2:0] mwa = 0;
  logic [12:0] mwd = 0;
  logic ov; logic [4:0] os; logic [23:0] ol, orr;
  KL_chan_map_capture #(.N_SLOTS_P(4), .N_TDM_P(8), .GAP_CYC_P(24),
                        .N_LB_STREAMS_P(1), .N_LB_CH_P(8)) u (
    .clk_i(clk), .rst_n(rst_n),
    .map_wr_en_i(mwe), .map_wr_addr_i(mwa), .map_wr_data_i(mwd),
    .map_rd_en_i(1'b0), .map_rd_addr_i(3'd0), .map_rd_data_o(), .map_rd_valid_o(),
    .map_flat_o(), .i2s_pair_valid_i(1'b0), .i2s_l_i(24'd0), .i2s_r_i(24'd0),
    .tdm_pair_valid_i(pv), .tdm_pair_slot_i(slot), .tdm_l_i(l), .tdm_r_i(r),
    .tone_smp_i(24'd0), .tick_i(tick),
    .pair_valid_o(ov), .pair_slot_o(os), .pair_l_o(ol), .pair_r_o(orr),
    .lb_dup_cnt_o(), .lb_skip_cnt_o(), .tdm_dup_cnt_o(), .tdm_skip_cnt_o());

  task automatic strobe(input int f, input int p);
    pv <= 1; slot <= 4'(p); l <= {8'(f), 8'(p), 8'h01}; r <= {8'(f), 8'(p), 8'h02};
    @(posedge clk); pv <= 0; @(posedge clk); @(posedge clk);
  endtask

  int got[4];
  // pair p of frame 2 strobed k cycles after the tick cycle (frame 2's other
  // pairs already delivered before the tick, pair 3 last when p != 3 is
  // measured on the base; on the head the close is what is measured)
  task automatic trial(input int p, input int k);
    int c, n;
    rst_n <= 0; repeat (4) @(posedge clk); rst_n <= 1; @(posedge clk);
    for (int ch = 0; ch < 8; ch++) begin
      mwe <= 1; mwa <= 3'(ch); mwd <= {1'b1, 1'(ch & 1), 3'd2, 4'd0, 4'(ch >> 1)};
      @(posedge clk);
    end
    mwe <= 0;
    for (int q = 0; q < 4; q++) strobe(1, q);
    for (int q = 0; q < 4; q++) if (q != p) strobe(2, q);
    repeat (4) @(posedge clk);
    tick <= 1; c = 0; n = 0;
    while (n < 4 && c < 400) begin
      if (c == k) begin pv <= 1; slot <= 4'(p); l <= {8'd2, 8'(p), 8'h01}; r <= {8'd2, 8'(p), 8'h02}; end
      else pv <= 0;
      @(posedge clk); tick <= 0; #1;
      if (ov) begin got[os] = int'(ol[23:16]); n++; end
      c++;
    end
    pv <= 0; repeat (4) @(posedge clk);
  endtask

  initial begin
    for (int p = 0; p < 4; p++) begin
      int last = -1;
      for (int k = 0; k < 130; k++) begin
        trial(p, k);
        if (got[p] == 2) last = k;
      end
      $display("pair %0d: a strobe at tick+0..tick+%0d reaches the walk the tick starts", p, last);
    end
    $finish;
  end
endmodule
`default_nettype wire
