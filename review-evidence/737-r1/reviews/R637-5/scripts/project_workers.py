#!/usr/bin/env python3
"""Recompute the sixteen-worker Verilator projection from a checkout's own tables.

Usage: python3 project_workers.py <checkout> [suite=seconds ...]
Prints each worker's projected seconds, its own 60% bound, the margin and its
units, using the checkout's scripts/suite_shards.py and generated rtl.yml.
Optional suite=seconds arguments override one duration (counterfactual)."""
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / "scripts"))
import suite_shards as s  # noqa: E402

seconds = dict(s.SUITE_SECONDS)
for arg in sys.argv[2:]:
    name, value = arg.split("=")
    seconds[name] = int(value)
suites = s.expand_suites(s.sweep_suites(root / "tb" / "verilator"))
total = len(s.WORKER_OVERHEAD_SECONDS)
owners, load = s.balance(suites, total, seconds)
limits = s.verilator_worker_limits((root / ".github/workflows/rtl.yml").read_text())
print(f"units={len(suites)} parents={len(s.sweep_suites(root / 'tb' / 'verilator'))} workers={total}")
print("gptp_tables owner:", owners.get("gptp_tables"), "seconds:", seconds.get("gptp_tables"))
for w in range(total):
    bound = limits[w] * 60 * s.HEADROOM_PERCENT // 100
    units = [u for u in suites if owners[u] == w]
    flag = "OK" if load[w] <= bound else "OVER"
    print(f"worker {w:2d}/{total}: {load[w]:5d} s  bound {bound:5d}  margin {bound - load[w]:5d}  {flag}  {' '.join(units)}")
