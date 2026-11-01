#!/usr/bin/env python3
"""Explicit start-and-stop witnesses, through the published model only, for cases
above the 96 and 192 kHz rows of the page's second fewer-reservations table.
Fixed terms are the page's. No timing here is a measurement.
Usage: python3 -I probe_r8_witness.py <mixed_stagger.py>
"""
import importlib.util, sys
from fractions import Fraction as Fr
spec = importlib.util.spec_from_file_location("published_model", sys.argv[1])
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
FIXED = {48: Fr(40325, 1000), 96: Fr(32491, 1000), 192: Fr(18093, 1000)}
P = {48: 6, 96: 12, 192: 24}

def run(name, khz, seq, page):
    rate = m.Rate(khz); ph = [[] for _ in range(P[khz])]; peak = 0; log = []
    for op in seq:
        if op[0] == "s":
            for _ in range(op[2]):
                log.append(m.greedy_add(rate, ph, op[1]))
        else:
            ph[op[1]].remove(op[2])
        peak = max(peak, sum(map(len, ph)))
    f = m.lindley_wait(rate, ph, None); e = m.cbs_sim(rate, ph, None)
    extra = ""
    if khz == 192:
        extra = f"; before the packetizer term {float(f + FIXED[192]):.3f}; packetizer as the model's queue, total {float(m.tandem_192(rate, ph, None)):.3f}"
        total = m.tandem_192(rate, ph, None)
    else:
        extra = f"; total {float(f + FIXED[khz]):.3f}"
        total = f + FIXED[khz]
    print(f"{name}: {khz} kHz start phases {log}; peak {peak}; final { {i: q for i, q in enumerate(ph) if q} }; "
          f"fifo {float(f):.3f}; 8.6.8.2 {float(e):.3f}{extra}; page row {page}; below 143.347: {float(total) < 143.347}")

first16_8 = [("x", p, 8) for p in (6, 3, 9, 1, 4, 7, 10, 2, 5, 8, 11)]
run("96 two eight-channel + one", 96, [("s", 8, 13)] + first16_8 + [("s", 1, 4), ("x", 6, 1), ("x", 3, 1), ("x", 9, 1)], "125.426")
run("48 three eight-channel + one", 48, [("s", 8, 13)] + [("x", p, 8) for p in (3, 1, 4, 2, 5)] * 2 + [("s", 1, 2), ("x", 3, 1)], "143.347")
run("192 six then one, adjacent", 192, [("s", 6, 1), ("s", 1, 8)] + [("x", p, 1) for p in (12, 6, 18, 3, 9, 15, 21)], "102.034")
run("192 eight then one, adjacent", 192, [("s", 8, 1), ("s", 1, 8)] + [("x", p, 1) for p in (12, 6, 18, 3, 9, 15, 21)], "102.034")
run("192 reviewer S1 placement", 192, [("s", 1, 4), ("s", 8, 1), ("x", 0, 1), ("x", 12, 1), ("x", 18, 1)], "102.034")
