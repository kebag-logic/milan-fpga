#!/usr/bin/env python3
"""Time one full ci_events check() of the pristine tree, N times, at a checkout.
Usage: time_contract_check.py <checkout> [N]"""
import sys, time, copy, pathlib
root = pathlib.Path(sys.argv[1]); n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
sys.path.insert(0, str(root / "scripts"))
import ci_events
world = ci_events.parse_world(ci_events.read_tree(root))
t = time.perf_counter()
for _ in range(n):
    w = copy.deepcopy(world)
    ci_events.check(w)
print(f"{root}: {(time.perf_counter() - t) / n:.3f} s per deepcopy+check over {n}")
