#!/usr/bin/env python3
"""Composition probe: rerun the candidate's 16-worker shard projection with
follow_ring at its table figure and scaled by the bind leg's measured 1.0709
(and, as a stress, by the slower-host ratio rounded up to 1.08 and 1.10).
Usage: shard_projection.py <repo>"""
import sys, math
from pathlib import Path
repo = Path(sys.argv[1]); sys.path.insert(0, str(repo / "scripts"))
import suite_shards as s
wf = (repo / ".github/workflows/rtl.yml").read_text()
suites = s.expand_suites(s.sweep_suites(repo / "tb/verilator"))
for label, factor in (("table", 1.0), ("bind x1.0709", 1.0709), ("x1.08", 1.08), ("x1.10", 1.10)):
    sec = dict(s.SUITE_SECONDS); sec["follow_ring"] = math.ceil(sec["follow_ring"] * factor)
    problems, load, bounds = s.headroom_problems(suites, wf, sec)
    owners, _ = s.balance(suites, len(bounds), sec, s.WORKER_OVERHEAD_SECONDS)
    w = owners["follow_ring"]
    mates = [x for x in suites if owners[x] == w]
    print(f"{label}: follow_ring={sec['follow_ring']} s on worker {w}, load {load[w]} s, "
          f"bound {bounds[w]} s, 1620 s budget, max non-dedicated load {max(load[:-1])} s; "
          f"problems={problems or 'none'}; mates={mates}")
