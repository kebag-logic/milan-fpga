#!/usr/bin/env python3
"""Emit the model's (hash_probe.py) worst 63-key window for S streams x C channels as a C++ initializer of
{stream, channel, cluster 0, cluster channel 0} mappings, and the visits the model predicts."""
import itertools, sys
sys.path.insert(0, sys.argv[1])
from hash_probe import slot, visits
S, C = int(sys.argv[2]), int(sys.argv[3])
keys = sorted(itertools.product(range(S), range(C)), key=lambda k: slot(*k))
best = max(((visits([keys[(i + j) % len(keys)] for j in range(63)]), i) for i in range(len(keys))))
window = [keys[(best[1] + j) % len(keys)] for j in range(63)]
print("// model visits", best[0])
print("{" + ",".join(f"{{{s},{c},0,0}}" for s, c in window) + "}")
