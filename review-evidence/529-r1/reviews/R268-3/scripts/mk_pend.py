#!/usr/bin/env python3
"""Disposable pending-bit-form RTL mutants of the Table 5.22 arbiter in
TREE/hdl/milan/milan_datapath.sv (one mutant per tree).
usage: mk_pend.py TREE NAME
  sout-n   the CRF pulse also raises STREAM_OUTPUT N_STREAMS (the CRF output)
  aaf-all  the CRF pulse also raises every AAF STREAM_INPUT row
  avb      the CRF pulse also raises AVB_INTERFACE 0
  ckd      the CRF pulse also raises CLOCK_DOMAIN 0
  stuck    the CRF STREAM_INPUT row's pending bit is never cleared
"""
import sys
tree, name = sys.argv[1], sys.argv[2]
p = tree + "/hdl/milan/milan_datapath.sv"
s = open(p).read()
R = {
 "sout-n": ("pp_ctr_sout_pend_n = pp_ctr_sout_pend_r | tkd_dirty_p_w;",
            "pp_ctr_sout_pend_n = pp_ctr_sout_pend_r | tkd_dirty_p_w"
            " | (ACMP_SRC_C'(crf_dirty_p_w) << N_STREAMS);"),
 "aaf-all": ("assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w};",
             "assign pp_ctr_sin_dirty_w = {crf_dirty_p_w, avtprx_dirty_p_w"
             " | {N_STREAMS{crf_dirty_p_w}}};"),
 "avb": ("pp_ctr_avb_pend_n  = pp_ctr_avb_pend_r  | ctr_avb_dirty_w;",
         "pp_ctr_avb_pend_n  = pp_ctr_avb_pend_r  | ctr_avb_dirty_w | crf_dirty_p_w;"),
 "ckd": ("pp_ctr_ckd_pend_n  = pp_ctr_ckd_pend_r  | ctr_ckd_dirty_w;",
         "pp_ctr_ckd_pend_n  = pp_ctr_ckd_pend_r  | ctr_ckd_dirty_w | crf_dirty_p_w;"),
 "stuck": ("          && (pp_ctr_evt_index_w == 16'(s))) pp_ctr_sin_pend_n[s] = 1'b0;",
           "          && (pp_ctr_evt_index_w == 16'(s)) && (s != N_STREAMS))"
           " pp_ctr_sin_pend_n[s] = 1'b0;"),
}
old, new = R[name]
assert s.count(old) == 1, (name, s.count(old))
open(p, "w").write(s.replace(old, new))
print("patched", name, p)
