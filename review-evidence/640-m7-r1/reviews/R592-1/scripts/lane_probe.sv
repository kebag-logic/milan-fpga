// Reviewer probe: exhaustive equivalence of the old and new byte-enable
// handling in KL_gptp_shadow for every legal lane count K = 1..8.
//
// TX: the old gearbox accumulated gb_keep_r[idx] <= 1 per byte (an index
// at or above K is an out-of-range write and is dropped) and stored
// st_keep = gb_keep_r | (K'(1) << idx). The new one stores the count
// CNT_W'(idx) + 1 and decodes keep[i] = (CNT_W'(i) < count). Every gearbox
// index 0..7 is checked, plus count 0 (an all-zero FIFO word) -> keep 0.
// RX: the old serializer took the highest set bit of the stored K-bit
// tkeep; the new FIFO stores that lane, computed by the same loop before
// the FIFO, in a 3-bit field. Every K-bit tkeep is checked, including
// non-contiguous and all-zero values, for range and round trip.
// Build: verilator --binary -Wno-fatal --top-module lane_probe lane_probe.sv
module lane_probe;
  int unsigned errors = 0;
  int unsigned checks = 0;

  for (genvar K = 1; K <= 8; K++) begin : g_k
    localparam int unsigned LANE_W_C = 3;
    localparam int unsigned CNT_W_C  = 4;
    initial begin : run
      logic [K-1:0] gb_keep, st_keep_old, keep_new, keep;
      logic [CNT_W_C-1:0] cnt;
      logic [LANE_W_C-1:0] top_new, top_old;
      // TX: one beat ending at each gearbox index
      for (int idx = 0; idx < 8; idx++) begin
        gb_keep = '0;
        for (int b = 0; b < idx; b++) if (b < K) gb_keep[b] = 1'b1;
        st_keep_old = gb_keep | (K'(1) << idx);
        cnt = CNT_W_C'(idx) + CNT_W_C'(1);
        for (int i = 0; i < K; i++) keep_new[i] = (CNT_W_C'(i) < cnt);
        checks++;
        if (keep_new !== st_keep_old) begin
          errors++;
          $display("TX K=%0d idx=%0d old=%b new=%b", K, idx, st_keep_old, keep_new);
        end
      end
      cnt = '0;
      for (int i = 0; i < K; i++) keep_new[i] = (CNT_W_C'(i) < cnt);
      checks++;
      if (keep_new !== '0) begin
        errors++;
        $display("TX K=%0d count 0 decodes to %b", K, keep_new);
      end
      // RX: every K-bit tkeep
      for (int v = 0; v < (1 << K); v++) begin
        keep = K'(v);
        top_new = '0;
        for (int i = 0; i < K; i++) if (keep[i]) top_new = LANE_W_C'(i);
        top_old = 3'd0;
        for (int i = 0; i < K; i++) if (keep[i]) top_old = 3'(i);
        checks++;
        if ((top_new !== top_old) || (int'(top_new) > K - 1)) begin
          errors++;
          $display("RX K=%0d keep=%b old=%0d new=%0d", K, keep, top_old, top_new);
        end
      end
    end
  end

  initial begin
    #1;
    $display("lane_probe: checks %0d errors %0d", checks, errors);
    if (errors != 0) $fatal(1, "lane_probe: FAIL");
    $display("lane_probe: PASS");
    $finish;
  end
endmodule
