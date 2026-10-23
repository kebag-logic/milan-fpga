#!/usr/bin/env python3
"""The servo's tracking unwrap, in 1/3 ns units (Ps = 62500): the dx form of
b23e9e31 against the sign-selected form, over every folded sample and a dense
sweep of references with their edges. Prints the mismatch count."""
import numpy as np
PS, H = 62500, 31250
x = np.arange(-H, H, dtype=np.int64)
refs = sorted(set(list(range(-H, H, 7)) + [-H, -H + 1, -1, 0, 1, H - 2, H - 1]))
bad = 0
for r in refs:
    dx = x - r
    dxf = np.where(dx >= H, dx - PS, np.where(dx < -H, dx + PS, dx))
    old = r + dxf
    up = r >= 0
    edge = r - H if up else r + H
    wrap = (x < edge) if up else (x >= edge)
    new = np.where(wrap, x + PS if up else x - PS, x)
    bad += int(np.count_nonzero(old != new))
print("refs", len(refs), "samples", len(x), "mismatches", bad)
