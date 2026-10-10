#!/usr/bin/env python3
"""Does lane B6's block_metrics give the loop's floor to 4 decimals at every rotation of the
1-second loop?  usage: rotation_floor.py <tools_dir> [count]"""
import collections
import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
import b6_thdn as A  # noqa: E402
import b6_tone as T6  # noqa: E402

n = int(sys.argv[2]) if len(sys.argv) > 2 else 120
lp = T6.loop().astype(np.float64)
rng = np.random.default_rng(5)
rots = sorted(set([0, 1, 12345, 24000, 47999] + list(rng.integers(0, 48000, n))))
for c, f in ((0, 997), (1, 9973)):
    cnt = collections.Counter()
    for r in rots:
        b = A.block_metrics(np.roll(lp[:, c], -int(r)), f)
        cnt[(round(float(b["thdn_db"]), 4), round(float(b["snr_db"]), 4))] += 1
    print(f"channel {c} {f} Hz over {len(rots)} rotations: {dict(cnt)}")
