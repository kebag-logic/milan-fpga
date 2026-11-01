#!/usr/bin/env python3
"""Reviewer probe: the published merge model's Pair, fed by hand. One network
only (an unpaired stream would behave the same: rule 2 does not apply), clean
for 20 packets, then copies with tu set whose sequence_num jumps by J (a talker
sequence discontinuity) while the head is still valid. Prints which rule acts
and where the samples land relative to the render buffer span.
Usage: python3 -I probe_merge_tu_seq_jump.py /path/to/merge_model.py
"""
import importlib.util, sys
spec = importlib.util.spec_from_file_location("mm", sys.argv[1]); mm = importlib.util.module_from_spec(spec); spec.loader.exec_module(mm)
for J in (+40, -40):
    p = mm.Pair(); p.c[0].clean_valid = False
    T0 = 10_000.0
    for j in range(20):
        p.copy(1, T0 + j * mm.T - mm.PTO + 100, T0 + j * mm.T, False, j, j)
    head_pos, dup0, w0 = p.head_pos, p.dup, p.writes
    now = T0 + 20 * mm.T - mm.PTO + 100
    p.copy(1, now, T0 + 20 * mm.T, True, (19 + J) % 256, 'jump')
    span_samples = int(mm.SPAN / mm.SP)
    if p.writes > w0:
        print(f"J={J:+d}: written at head_pos{p.head_pos - head_pos:+d} samples (render buffer span {span_samples} samples); head_valid={p.head_valid}")
    else:
        print(f"J={J:+d}: not written; counted as duplicate: {p.dup - dup0 == 1}")
