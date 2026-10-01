#!/usr/bin/env python3
"""Count restarts per step case (page row: 'Each restarts the history exactly once')."""
import sys, collections
sys.path.insert(0, sys.argv[1])
import loss_rule_model as L
hist = collections.Counter()
for size in [L.ONE, -L.ONE, L.HALF, -L.HALF]:
    for pos in range(16):
        for seed in range(4):
            g = 2000
            lostp = g * 16 + (0 if pos == 15 else 15)
            m = L.run(2100, 300, L.shape("random_sign_group", 1426, 100 + seed), frozenset([lostp]),
                      None, step=(g * 16 + pos, size))
            hist[m.restarts] += 1
print("restart-count histogram over 256 step cases:", dict(hist))
