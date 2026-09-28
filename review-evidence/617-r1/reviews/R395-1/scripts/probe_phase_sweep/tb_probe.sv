// Reviewer probe R395-1 (PR #618 / issue #617). Not part of the tree.
//
// Two instances of KL_chan_map_capture at the shipping 1x1 TDM8 parameters
// (N_SLOTS_P=4, N_TDM_P=8, LOOP 1 stream x 8 ch, GAP_CYC_P=24):
//   u4: TDM_FRAME_PAIRS_P=4. Frame A (pairs 0..3) is published, then frame B's
//       pairs 0..2 are staged; a tick starts a walk and frame B's closing pair
//       3 is strobed K cycles after the tick, for EVERY K from 0 to past the
//       walk's end. Every walk column must be all-A or all-B (never mixed);
//       the column of the NEXT walk must be all-B; a close strictly before
//       the snapshot must be visible to this walk (no added frame).
//   u1: TDM_FRAME_PAIRS_P=1, the I2S shapes' one-pair frame: only pair 0 is
//       ever strobed (KL_aaf_capture_i2s parks at slot 0) and the channel
//       map selects SRC=TDM idx 0. The walk must carry the latest pair.
`default_nettype none
module tb_probe;
  logic clk = 0;
  always #5 clk = ~clk;
  logic rst_n = 0;

  logic        pv4 = 0, pv1 = 0, tick4 = 0, tick1 = 0;
  logic [3:0]  slot4 = 0;
  logic [23:0] l4 = 0, r4 = 0, l1 = 0, r1 = 0;
  logic        mwe = 0;
  logic [2:0]  mwa = 0;
  logic [12:0] mwd = 0;

  logic        o4_v, o1_v;
  logic [4:0]  o4_s, o1_s;
  logic [23:0] o4_l, o4_r, o1_l, o1_r;

  KL_chan_map_capture #(.N_SLOTS_P(4), .N_TDM_P(8), .TDM_FRAME_PAIRS_P(4),
                        .GAP_CYC_P(24), .N_LB_STREAMS_P(1), .N_LB_CH_P(8)) u4 (
    .clk_i(clk), .rst_n(rst_n),
    .map_wr_en_i(mwe), .map_wr_addr_i(mwa), .map_wr_data_i(mwd),
    .map_rd_en_i(1'b0), .map_rd_addr_i(3'd0), .map_rd_data_o(), .map_rd_valid_o(),
    .map_flat_o(),
    .i2s_pair_valid_i(1'b0), .i2s_l_i(24'd0), .i2s_r_i(24'd0),
    .tdm_pair_valid_i(pv4), .tdm_pair_slot_i(slot4), .tdm_l_i(l4), .tdm_r_i(r4),
    .tone_smp_i(24'd0), .tick_i(tick4),
    .pair_valid_o(o4_v), .pair_slot_o(o4_s), .pair_l_o(o4_l), .pair_r_o(o4_r),
    .lb_dup_cnt_o(), .lb_skip_cnt_o(), .tdm_dup_cnt_o(), .tdm_skip_cnt_o());

  KL_chan_map_capture #(.N_SLOTS_P(4), .N_TDM_P(8), .TDM_FRAME_PAIRS_P(1),
                        .GAP_CYC_P(24), .N_LB_STREAMS_P(1), .N_LB_CH_P(8)) u1 (
    .clk_i(clk), .rst_n(rst_n),
    .map_wr_en_i(mwe), .map_wr_addr_i(mwa), .map_wr_data_i(mwd),
    .map_rd_en_i(1'b0), .map_rd_addr_i(3'd0), .map_rd_data_o(), .map_rd_valid_o(),
    .map_flat_o(),
    .i2s_pair_valid_i(pv1), .i2s_l_i(l1), .i2s_r_i(r1),
    .tdm_pair_valid_i(pv1), .tdm_pair_slot_i(4'd0), .tdm_l_i(l1), .tdm_r_i(r1),
    .tone_smp_i(24'd0), .tick_i(tick1),
    .pair_valid_o(o1_v), .pair_slot_o(o1_s), .pair_l_o(o1_l), .pair_r_o(o1_r),
    .lb_dup_cnt_o(), .lb_skip_cnt_o(), .tdm_dup_cnt_o(), .tdm_skip_cnt_o());

  int checks = 0, fails = 0;
  task automatic ck(input bit ok, input string what);
    checks++;
    if (!ok) begin fails++; $display("[FAIL] %s", what); end
  endtask

  // frame f, pair p: L = {8'hA0|f, 8'(p), 8'h01}, R = {..., 8'h02}
  function automatic logic [23:0] fl(input int f, input int p);
    return {8'(8'hA0 + f), 8'(p), 8'h01};
  endfunction
  function automatic logic [23:0] fr(input int f, input int p);
    return {8'(8'hA0 + f), 8'(p), 8'h02};
  endfunction

  task automatic strobe4(input int f, input int p);
    pv4 <= 1; slot4 <= 4'(p); l4 <= fl(f, p); r4 <= fr(f, p);
    @(posedge clk); pv4 <= 0;
    @(posedge clk); @(posedge clk);
  endtask

  // map: channel c -> SRC=TDM (2), half c&1, idx c>>1, on both instances
  task automatic program_map();
    for (int c = 0; c < 8; c++) begin
      mwe <= 1; mwa <= 3'(c);
      mwd <= {1'b1, 1'(c & 1), 3'd2, 4'd0, 4'(c >> 1)};
      @(posedge clk);
    end
    mwe <= 0; @(posedge clk);
  endtask

  // collect one walk of u4 (4 slots): frame tag of each slot's L and R
  int wf[8];
  int nseen;
  task automatic reset_dut();
    rst_n <= 0; pv4 <= 0; pv1 <= 0; tick4 <= 0; tick1 <= 0;
    repeat (4) @(posedge clk);
    rst_n <= 1; @(posedge clk);
    program_map();
  endtask

  // one walk of u4 started by a tick; pair 3 of frame `fb` is strobed `k`
  // cycles after the tick cycle (k = 0: in the tick cycle itself)
  task automatic walk_with_close_at(input int k, input int fb);
    int c; bit closed;
    nseen = 0; closed = 0;
    tick4 <= 1;
    c = 0;
    while (nseen < 4 && c < 400) begin
      if (c == k) begin pv4 <= 1; slot4 <= 4'd3; l4 <= fl(fb, 3); r4 <= fr(fb, 3); closed = 1; end
      else pv4 <= 0;
      @(posedge clk);
      tick4 <= 0;
      #1;
      if (o4_v) begin
        wf[2 * int'(o4_s)]     = int'(o4_l[23:16]) - 8'hA0;
        wf[2 * int'(o4_s) + 1] = int'(o4_r[23:16]) - 8'hA0;
        ck(o4_l[15:8] == 8'(o4_s) && o4_r[15:8] == 8'(o4_s), $sformatf("k=%0d slot %0d carries its own pair", k, o4_s));
        nseen++;
      end
      c++;
    end
    pv4 <= 0;
    // if the close was not yet issued inside the walk, issue it now
    if (!closed) begin
      pv4 <= 1; slot4 <= 4'd3; l4 <= fl(fb, 3); r4 <= fr(fb, 3);
      @(posedge clk); pv4 <= 0;
    end
    repeat (8) @(posedge clk);
  endtask

  int kmax;
  int first_b = -1;
  int last_a = -1;
  int changes = 0;
  int prev_b = -1;
  int first_a = -1;
  initial begin
    // ---------------- u4: every close offset across one walk ----------------
    // walk = 1 idle + (LB_PAIRS_C+1)=5 pop + 4 x 26 slot cycles = 110 cycles
    kmax = 130;
    for (int k = 0; k <= kmax; k++) begin
      bit all_a, all_b;
      reset_dut();
      for (int p = 0; p < 4; p++) strobe4(1, p);   // frame 1 (A) closed
      for (int p = 0; p < 3; p++) strobe4(2, p);   // frame 2 (B) staged
      repeat (4) @(posedge clk);
      walk_with_close_at(k, 2);
      ck(nseen == 4, $sformatf("k=%0d walk emitted 4 slots", k));
      all_a = 1; all_b = 1;
      for (int i = 0; i < 8; i++) begin
        all_a &= (wf[i] == 1);
        all_b &= (wf[i] == 2);
      end
      ck(all_a || all_b, $sformatf("k=%0d walk column is one frame (got %0d %0d %0d %0d %0d %0d %0d %0d)",
                                   k, wf[0], wf[1], wf[2], wf[3], wf[4], wf[5], wf[6], wf[7]));
      if (all_b && first_b < 0) first_b = k;
      if (all_a) last_a = k;
      if (all_a && first_a < 0) first_a = k;
      if (prev_b >= 0 && int'(all_b) != prev_b) changes++;
      prev_b = int'(all_b);
      // the next walk must read frame B whole
      walk_with_close_at(1000, 3);   // k beyond the walk: close issued after
      begin
        bit nb = 1;
        for (int i = 0; i < 8; i++) nb &= (wf[i] == 2);
        ck(nb, $sformatf("k=%0d next walk reads frame B whole", k));
      end
    end
    begin
      int lb = -1;
      for (int k = 0; k <= kmax; k++) ;
      $display("[i] u4: a close strobed at tick+0..tick+%0d reaches that walk; tick+%0d..tick+%0d waits for the next (transitions=%0d)",
               first_a - 1, first_a, last_a, changes);
    end
    ck(first_b == 0, "u4: a close in the tick cycle itself is visible to that walk");
    ck(last_a == kmax, "u4: a close after the walk waits for the next walk");
    ck(changes == 1, $sformatf("u4: exactly one B->A transition across the offsets (got %0d)", changes));

    // ---------------- u1: the one-pair frame (I2S shapes) ----------------
    reset_dut();
    for (int n = 1; n <= 3; n++) begin
      pv1 <= 1; l1 <= fl(n, 0); r1 <= fr(n, 0);
      @(posedge clk); pv1 <= 0;
      repeat (3) @(posedge clk);
      tick1 <= 1; @(posedge clk); tick1 <= 0;
      nseen = 0;
      for (int c = 0; c < 200 && nseen < 4; c++) begin
        @(posedge clk); #1;
        if (o1_v) begin
          if (o1_s == 0) begin
            ck(o1_l == fl(n, 0) && o1_r == fr(n, 0),
               $sformatf("u1 one-pair frame: walk %0d slot 0 carries the latest pair (got %h %h)", n, o1_l, o1_r));
          end
          nseen++;
        end
      end
      repeat (8) @(posedge clk);
    end

    $display("== probe: checks: %0d failures: %0d ==", checks, fails);
    $display("%s", fails == 0 ? "RESULT: PASS" : "RESULT: FAIL");
    $finish;
  end
endmodule
`default_nettype wire
