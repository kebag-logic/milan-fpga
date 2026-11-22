#!/usr/bin/env python3
"""Probe (reviewer, disposable): insert tap-side bubbles inside each frame.

Usage: plant_tap_bubbles.py <tree>   (a disposable copy of the head tree)

sim_depkt.cpp: before each beat, 0-3 stall cycles (60% of beats), each either
tvalid low or tvalid high with s_tready_i low; the enqueue pulse is scheduled
from the cycle the eighth beat is ACCEPTED, at the bench's enq_lat.
sim_fanout.cpp: before each beat, 0-3 cycles of tvalid low (the wrap ties the
tap's tready high), through the real parser and monitor.
Each edit must match exactly once; exit 1 otherwise.
"""
import sys
from pathlib import Path

T = Path(sys.argv[1]) / "tb/verilator/avtp_rxmon"

def sub(p, old, new):
    s = p.read_text()
    if s.count(old) != 1:
        print("anchor not unique in", p, repr(old[:60])); sys.exit(1)
    p.write_text(s.replace(old, new))

LCG = ("static unsigned bub_lcg() { static unsigned x = 0x9e3779b9u; x = x * 1664525u + 1013904223u; "
       "return x >> 8; }\n")

d = T / "sim_depkt.cpp"
sub(d, "            if (fr.queued && b == 7) enq_owed.push_back(Enq{now + enq_lat, fr.mask, lag});\n            cycle();\n",
       "            d->s_tlast_i = b + 1 == beats;\n"
       "            if (bub_lcg() % 10 < 6) {\n"
       "                const unsigned nb = 1 + bub_lcg() % 3;\n"
       "                for (unsigned i = 0; i < nb; i++) {\n"
       "                    if (bub_lcg() & 1) { d->s_tvalid_i = 0; d->s_tready_i = 1; }\n"
       "                    else               { d->s_tvalid_i = 1; d->s_tready_i = 0; }\n"
       "                    cycle();\n"
       "                }\n"
       "                d->s_tvalid_i = 1; d->s_tready_i = 1;\n"
       "            }\n"
       "            if (fr.queued && b == 7) enq_owed.push_back(Enq{now + enq_lat, fr.mask, lag});\n            cycle();\n")
s = d.read_text()
i = s.index("#include")
j = s.index("\n", s.rindex("#include")) + 1
d.write_text(s[:j] + LCG + s[j:])

f = T / "sim_fanout.cpp"
sub(f, "            dut->s_tvalid_i = 1;\n            dut->s_tlast_i = (b == beats - 1);\n            cyc();\n",
       "            if (bub_lcg() % 10 < 6) {\n"
       "                dut->s_tvalid_i = 0;\n"
       "                cyc(static_cast<int>(1 + bub_lcg() % 3));\n"
       "            }\n"
       "            dut->s_tvalid_i = 1;\n            dut->s_tlast_i = (b == beats - 1);\n            cyc();\n")
s = f.read_text()
j = s.index("\n", s.rindex("#include")) + 1
f.write_text(s[:j] + LCG + s[j:])
print("planted tap bubbles in", d, "and", f)
