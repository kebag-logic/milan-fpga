#!/usr/bin/env python3
"""Disposable mutant: exchange the root wires of two KL_crf_rx output ports
at the crf_rx instance in TREE/hdl/milan/milan_datapath.sv.
usage: mk_swap.py TREE PORT_A PORT_B      (e.g. cnt_locked_o cnt_unlocked_o)
       mk_swap.py --list                  (the ten ports, one per line)"""
import re, sys
PORTS = {  # port -> (root wire, Table 7-157 quadlet)
    "cnt_locked_o": ("crf_lockcnt_w", 0), "cnt_unlocked_o": ("crf_unlockcnt_w", 1),
    "cnt_intr_o": ("crf_intrcnt_w", 2), "seq_err_o": ("crf_seqerr_w", 3),
    "mr_cnt_o": ("crf_mrcnt_w", 4), "tu_cnt_o": ("crf_tucnt_w", 5),
    "fmt_err_o": ("crf_fmterr_w", 8), "late_cnt_o": ("crf_latecnt_w", 9),
    "early_cnt_o": ("crf_earlycnt_w", 10), "pdu_count_o": ("crf_pducnt_w", 11),
}
if sys.argv[1] == "--list":
    for k in PORTS: print(k, PORTS[k][1])
    sys.exit(0)
tree, pa, pb = sys.argv[1:4]
p = tree + "/hdl/milan/milan_datapath.sv"
s = open(p).read()
i0 = s.index(") crf_rx (")
i1 = s.index(");", s.index(".dirty_p_o", i0))
blk = s[i0:i1]
for port in (pa, pb):
    n = len(re.findall(r"\.%s\s*\(\s*%s\s*\)" % (port, PORTS[port][0]), blk))
    assert n == 1, (port, n)
wa, wb = PORTS[pa][0], PORTS[pb][0]
blk = re.sub(r"(\.%s\s*\(\s*)%s(\s*\))" % (pa, wa), r"\1@@A@@\2", blk)
blk = re.sub(r"(\.%s\s*\(\s*)%s(\s*\))" % (pb, wb), r"\1%s\2" % wa, blk)
blk = blk.replace("@@A@@", wb)
open(p, "w").write(s[:i0] + blk + s[i1:])
print("swapped", pa, pb)
