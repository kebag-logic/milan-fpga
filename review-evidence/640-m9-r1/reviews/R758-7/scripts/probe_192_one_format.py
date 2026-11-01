#!/usr/bin/env python3
"""One format N=8 at 192 kHz from a fresh port, the case the 16-reservation row omits.
Usage: python3 -I probe_192_one_format.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from probe_fewer_bound import FIXED, Rate

r = Rate(192)
for count in range(14, 0, -1):
    ph = [[] for _ in range(r.P)]
    for _ in range(count):
        r.start(ph, 8)
    w = float(r.wait(ph))
    print(f"192 kHz N=8, {count} streams: wait {w:.3f} us; with the page's largest fixed terms {w + FIXED[192][1]:.3f} us")
