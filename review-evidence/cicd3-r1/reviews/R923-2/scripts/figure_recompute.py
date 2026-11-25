#!/usr/bin/env python3
"""Recomputes each new piece figure of PR #1003 from the derivation table it publishes
(old figure x new local wall / old local wall, rounded up) and compares with suite_shards.PIECE_SECONDS.
usage: figure_recompute.py REPO"""
import math, sys
sys.path.insert(0, sys.argv[1] + "/scripts")
from suite_shards import PIECE_SECONDS
ROWS = [("milan_dp", 0, 1309, 463.8, 953.5), ("milan_dp", 1, 1313, 710.5, 809.8), ("milan_dp", 2, 275, 148.2, 281.7),
        ("milan_dp", 3, 399, 221.6, 403.1), ("milan_dp", 4, 1309, 741.6, 953.5), ("milan_dp", 5, 1313, 222.9, 809.8),
        ("milan_dp", 6, 275, 153.2, 281.7), ("milan_dp", 7, 399, 245.0, 403.1),
        ("capture_coherence", 0, 1618, 581.6, 859.7), ("capture_coherence", 1, 1204, 467.0, 632.2),
        ("capture_coherence", 2, 695, 220.4, 440.8), ("capture_coherence", 3, 724, 235.6, 415.4),
        ("capture_coherence", 4, 1618, 223.5, 859.7), ("capture_coherence", 5, 1204, 225.6, 632.2),
        ("capture_coherence", 6, 695, 217.8, 440.8), ("capture_coherence", 7, 724, 259.9, 415.4),
        ("follow_ring", 0, 1493, 378.0, 959.5), ("follow_ring", 1, 1493, 690.7, 959.5),
        ("media_phase", 0, 1400, 263.6, 755.1), ("media_phase", 1, 1400, 262.4, 755.1), ("media_phase", 2, 1400, 282.3, 755.1)]
for suite, leg, old, new_wall, old_wall in ROWS:
    raw = old * new_wall / old_wall
    tree = PIECE_SECONDS[suite][leg]
    print(f"{suite}__{leg:<2} tree {tree:5}  table {raw:8.2f} ceil {math.ceil(raw):5}  "
          f"{'OK' if tree == math.ceil(raw) else 'tree is %+d over the rounded-up table value' % (tree - math.ceil(raw))}")
