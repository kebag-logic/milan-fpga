"""Sampler wake spacing in the step 1 board sampler record (first field of each line, seconds).
usage: sampler_spacing.py <name.samp>"""
import re, sys
import numpy as np
up = np.array([float(m.group(1)) for m in (re.match(r"^([0-9.]+) [0-9.]+$", l) for l in open(sys.argv[1])) if m])
d = np.diff(up)
print("wakes", len(up), "spacing min %.4f max %.4f median %.4f" % (d.min(), d.max(), np.median(d)))
print("spacings below 1.02 s:", int((d < 1.015).sum()), "; above 1.04 s:", int((d > 1.045).sum()))
