#!/usr/bin/env python3
"""Pool the RAW lock times of receipts/locktime_pop and give, per loss rate,
the population median and quartiles and the 2.5-97.5 % range of the median
of 32 seeds drawn from the population (bootstrap), against the page's
32-seed figures."""
import glob, re, sys
import numpy as np
page = {"8": (7.8, 7.3, 11.4, 26.3), "11.2": (17.3, 10.4, 26.8, 37.0),
        "16": (29.1, 16.0, 41.1, 74.9), "24": (288, 159, 387, 968)}
rng = np.random.default_rng(7)
for lost in ("8", "11.2", "16", "24"):
    xs = []
    for f in sorted(glob.glob(f"receipts/locktime_pop/lost_{lost}_j*.out")):
        for line in open(f):
            if line.startswith("RAW"):
                xs += [float(v) for v in line.split()[1:]]
    x = np.array(xs)
    fin = np.isfinite(x)
    q = np.percentile(x[fin], [25, 50, 75])
    meds = np.median(rng.choice(x, (20000, 32)), axis=1)
    q25s = np.percentile(rng.choice(x, (20000, 32)), 25, axis=1)
    lo, hi = np.percentile(meds, [2.5, 97.5])
    pm = page[lost]
    pr = np.mean(meds <= pm[0]) if pm[0] < q[1] else np.mean(meds >= pm[0])
    print(f"lost/s {lost}: n {len(x)} never-locked {np.sum(~fin)}; population median {q[1]:.1f} s, "
          f"quartiles {q[0]:.1f}-{q[2]:.1f} s, max {x[fin].max():.1f} s; 32-seed median 95 % range "
          f"{lo:.1f}-{hi:.1f} s; page median {pm[0]} (one-sided tail {pr:.3f}), page middle half {pm[1]}-{pm[2]}, slowest {pm[3]}")
