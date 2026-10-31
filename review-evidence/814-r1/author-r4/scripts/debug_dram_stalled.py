#!/usr/bin/env python3
"""debug_dram_stalled.py <repo>/sw/litex: dram_stalled on the wired build, each issued-against-seen list compared."""
import sys
import time

sys.path.insert(0, sys.argv[1])
import test_soc_timing_cuts as t  # noqa: E402

start = time.time()
got = t.dram_stalled(t.WirePassThrough, 814)
print(f"{time.time() - start:.0f} s, timeout {got['timeout']}")
for key in ("writes", "wdata", "reads", "rdata"):
    a, b = got[key], got[f"issued_{key}"]
    print(key, a == b, len(a), len(b))
    if a != b:
        print("  seen  ", [hex(x)[:12] for x in a])
        print("  issued", [hex(x)[:12] for x in b])
