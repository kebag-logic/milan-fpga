#!/usr/bin/env python3
"""Disposable probe: patch TREE/hdl/milan/milan_datapath.sv so the Table 5.22
descriptor arbiter's scalar face can hand the processor ONE extra tuple
{GHOST_TY, GHOST_IX} for each CRF dirty pulse, chosen at run time:

  +GHOST=1          arm the extra tuple (default 0: byte-for-byte behaviour
                    of the unmutated arbiter on the face)
  +GHOST_TY=<hex>   its descriptor_type   (16 bits)
  +GHOST_IX=<hex>   its descriptor_index  (16 bits)
  +GHOST_REPLACE=1  also drop the CRF pulse from the STREAM_INPUT row, so the
                    extra tuple is the ONLY delivery the pulse produces

The arbiter's own pick / pending / round-robin logic is untouched: it is
renamed pp_ctr_arb_*, and the face (pp_ctr_evt_*_w, which the harness
observes and KL_pp_shadow consumes) carries the arbiter's tuple when it has
one, else the ghost. The ghost never clears a pending bit or moves the
round-robin pointer. usage: mk_ghost.py TREE
"""
import sys, re
p = sys.argv[1] + "/hdl/milan/milan_datapath.sv"
s = open(p).read()
a = s.index("always_comb begin : pp_ctr_event_pick")
b = s.index("end : pp_ctr_event_queue") + len("end : pp_ctr_event_queue")
blk = s[a:b]
n0 = blk.count("pp_ctr_evt_")
blk = (blk.replace("pp_ctr_evt_valid_w", "pp_ctr_arb_valid_w")
          .replace("pp_ctr_evt_type_w", "pp_ctr_arb_type_w")
          .replace("pp_ctr_evt_index_w", "pp_ctr_arb_index_w"))
assert "pp_ctr_evt_" not in blk and n0 > 10, n0
ghost = """
  // ---- R268-3 PROBE (disposable): the ghost tuple's face ----
  wire ghost_go_w = ghost_pend_r && !pp_ctr_arb_valid_w;
  always_ff @(posedge axis_clk or negedge axis_resetn) begin : ghost_q
    if (!axis_resetn) ghost_pend_r <= 1'b0;
    else ghost_pend_r <= (ghost_pend_r && !ghost_go_w)
                      || (crf_dirty_p_w && (ghost_en_c != 0));
  end : ghost_q
  assign pp_ctr_evt_valid_w = pp_ctr_arb_valid_w || ghost_go_w;
  assign pp_ctr_evt_type_w  = pp_ctr_arb_valid_w ? pp_ctr_arb_type_w  : ghost_ty_c;
  assign pp_ctr_evt_index_w = pp_ctr_arb_valid_w ? pp_ctr_arb_index_w : ghost_ix_c;
"""
s = s[:a] + blk + "\n" + ghost + s[b:]
decl = """  // ---- R268-3 PROBE (disposable): the ghost tuple's run-time choice ----
  logic        pp_ctr_arb_valid_w;
  logic [15:0] pp_ctr_arb_type_w, pp_ctr_arb_index_w;
  logic [15:0] ghost_ty_c, ghost_ix_c;
  logic [31:0] ghost_en_c, ghost_rep_c;
  logic        ghost_pend_r;
  initial begin
    if (!$value$plusargs("GHOST=%d", ghost_en_c))          ghost_en_c  = 0;
    if (!$value$plusargs("GHOST_TY=%h", ghost_ty_c))       ghost_ty_c  = 16'h0;
    if (!$value$plusargs("GHOST_IX=%h", ghost_ix_c))       ghost_ix_c  = 16'h0;
    if (!$value$plusargs("GHOST_REPLACE=%d", ghost_rep_c)) ghost_rep_c = 0;
  end
"""
anchor = "  wire  [PP_CTR_SIN_N_C-1:0] pp_ctr_sin_dirty_w;"
assert s.count(anchor) == 1
s = s.replace(anchor, decl + anchor)
old = "assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};"
assert s.count(old) == 1
s = s.replace(old, "assign pp_ctr_sin_dirty_w = {crf_dirty_p_w && (ghost_rep_c == 0), avtprx_dirty_p_w};")
open(p, "w").write(s)
print("patched", p)
