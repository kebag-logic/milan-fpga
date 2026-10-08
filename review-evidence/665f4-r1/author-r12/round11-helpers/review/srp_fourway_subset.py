#!/usr/bin/env python3
"""Run the author's four-way-* SRP plants (srp_mutants.DEFECTS)
at one interface count, partition K of N, with the repository's own campaign.
usage: srp_plants_subset.py REPO LWSRP WORK IFCOUNT K N
"""
import sys
from pathlib import Path
repo, lwsrp, work = (Path(a).resolve() for a in sys.argv[1:4])
ifs, k, n = (int(a) for a in sys.argv[4:7])
sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]
import srp_mutants
chosen = [d for d in srp_mutants.DEFECTS if d.name.startswith(("four-way-",))]
srp_mutants.DEFECTS = tuple(chosen[k::n])
print(f"partition {k}/{n} at IF={ifs}: {[d.name for d in srp_mutants.DEFECTS]}", flush=True)
sys.exit(1 if srp_mutants.campaign(work, lwsrp, 4, ifs) else 0)
