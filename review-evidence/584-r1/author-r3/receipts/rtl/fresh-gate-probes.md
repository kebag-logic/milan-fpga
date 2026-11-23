# Freshness-gate isolation probes

These preliminary probes expose a limit of the shipping-shape test. The render stage already flushes the fallen stream; forcing the later freshness gate open does not replay a sample on its own. Both probes pass 130 checks. The replay arms in the final campaign explicitly deliver stale events and fail B3/Z3 FRESHNESS. Passing these isolation probes is not a mutation catch.

The mutated RTL sources stay in scratch; only source hashes, sizes and focused diffs are included. Baseline RTL is unchanged through head 599c79af.

## open
Planted source: 559003 bytes; sha256 `0ffaab26dc65d1bab2949475ff0f47813aaa605d56c2a523b334d27b56030d51`.
```diff
--- hdl/milan/milan_datapath.sv
+++ planted.sv
@@ -8659,7 +8659,7 @@
   end : tdm_lane_freshness
   //! a lane with no mapped stream has nothing to be stale about, so the
   //! reduction is over the mapped streams only
-  wire tdmr_fresh_w = &(tdmr_fresh_r | ~tdmr_lane_streams_w);
+  wire tdmr_fresh_w = 1'b1;
 
   generate if (AUDIO_IF_RENDER_SLOTS_P == 0) begin : g_tdm_render_parked
     //! No render lane on this build: the serial output is driven low and the
```
Runtime output: `fresh-gate-open.log`.

## uncleared
Planted source: 558971 bytes; sha256 `28a72edc6171731b960ccb11b7fadea06c3eae95364cfb7b1f6f5807a153894e`.
```diff
--- hdl/milan/milan_datapath.sv
+++ planted.sv
@@ -8652,8 +8652,7 @@
     if (!axis_resetn) tdmr_fresh_r <= '0;
     else begin
       for (int s = 0; s < N_STREAMS; s++) begin
-        if (strtbl_bind_fall_w[s])  tdmr_fresh_r[s] <= 1'b0;
-        else if (rq_pop_p_w[s])     tdmr_fresh_r[s] <= 1'b1;
+        if (rq_pop_p_w[s])     tdmr_fresh_r[s] <= 1'b1;
       end
     end
   end : tdm_lane_freshness
```
Runtime output: `fresh-gate-uncleared.log`.

