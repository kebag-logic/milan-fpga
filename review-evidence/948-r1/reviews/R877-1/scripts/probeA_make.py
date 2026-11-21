#!/usr/bin/env python3
"""Probe A: copy the head's KL_aaf_rx_depacketizer.sv and add occupancy monitors
(verdict queue, read-side queue, done-before-enqueue) that print PROBE lines.
usage: probeA_make.py SRC OUT"""
import sys
from pathlib import Path
src, out = Path(sys.argv[1]), Path(sys.argv[2])
t = src.read_text()
anchor = "  end : verdict_queue\n"
assert t.count(anchor) == 1
probe = anchor + r'''
  // ---- disposable review probe (not part of the design) ----
  logic [RQ_LOG2_C:0] pr_rq_max_r; logic [IDXQ_LOG2_C-1:0] pr_iq_max_r;
  wire [RQ_LOG2_C:0] pr_rq_occ_w = rq_ap_r - rq_rp_r;
  wire [IDXQ_LOG2_C-1:0] pr_iq_occ_w = idxq_wp_r - idxq_rp_r;
  always_ff @(posedge clk_i) begin : review_probe
    if (!rst_n) begin pr_rq_max_r <= '0; pr_iq_max_r <= '0; end
    else begin
      if (pr_rq_occ_w > pr_rq_max_r) begin pr_rq_max_r <= pr_rq_occ_w; $display("PROBE-RQ-MAX %0d", pr_rq_occ_w); end
      if (pr_iq_occ_w > pr_iq_max_r) begin pr_iq_max_r <= pr_iq_occ_w; $display("PROBE-IQ-MAX %0d", pr_iq_occ_w); end
      if (pdu_enq_p_i && (pr_rq_occ_w == 3'(1 << RQ_LOG2_C)) && !retire_w) $display("PROBE-RQ-OVERFLOW");
      if (pr_rq_occ_w > 3'(1 << RQ_LOG2_C)) $display("PROBE-RQ-OCC-ILLEGAL %0d", pr_rq_occ_w);
      if (pdu_done_p_i && (rq_vp_r == rq_ap_r)) $display("PROBE-DONE-WITHOUT-ENQ");
      if ((rq_vp_r - rq_rp_r) > (rq_ap_r - rq_rp_r)) $display("PROBE-VP-PAST-AP");
      if (idxq_pop_w && !sq_ne_w) $display("PROBE-IQ-UNDERFLOW");
    end
  end : review_probe
'''
out.write_text(t.replace(anchor, probe))
