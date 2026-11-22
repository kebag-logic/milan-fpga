#!/usr/bin/env python3
"""Probe B: copy the head's milan_datapath.sv with the per-input 5.3.8.7 stop
gate replaced by a shared one: a stopped input among a PDU's accepting inputs
discards the PDU for all of them. usage: probeB_make.py SRC OUT"""
import sys
from pathlib import Path
src, out = Path(sys.argv[1]), Path(sys.argv[2])
t = src.read_text()
old = "      avtprx_done_mask_w & ~acmpl_stopped_v_w[N_STREAMS-1:0];\n"
new = ("      avtprx_done_mask_w & ~{N_STREAMS{|(avtprx_done_mask_w &"
       " acmpl_stopped_v_w[N_STREAMS-1:0])}};\n")
assert t.count(old) == 1, t.count(old)
out.write_text(t.replace(old, new))
