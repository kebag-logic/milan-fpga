#!/usr/bin/env python3
"""r582_pub_plants.py - R582-3: the author's publication plants only, with the gate's own campaigns.

Usage: r582_pub_plants.py <checkout> <lwsrp> <scratch-root>

Runs ctrl_mutants.campaign over the table's publication entries (names with
"pub-" or starting "rv-maap-") and srp_mutants.campaign over srp_pub_mutants'
table at two interfaces. Read-only on <checkout>.
"""
import sys
from pathlib import Path

checkout, lwsrp, root = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import ctrl_mutants  # noqa: E402
import srp_mutants  # noqa: E402
import srp_pub_mutants  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

reuse = root / "reuse"
cut_reuse(reuse)
ctrl_mutants.MUTANTS = tuple(m for m in ctrl_mutants.MUTANTS if "pub-" in m.name or m.name.startswith("rv-maap-"))
ctrl_mutants.unnamed_tests = lambda *a, **k: []      # the full gate checks that every test is named
print(f"ctrl publication plants: {len(ctrl_mutants.MUTANTS)}", flush=True)
bad = ctrl_mutants.campaign(root / "ctrl", reuse, 4)
srp_mutants.DEFECTS = srp_pub_mutants.defects(srp_mutants.Defect)
print(f"SRP publication plants: {len(srp_mutants.DEFECTS)}", flush=True)
bad = srp_mutants.campaign(root / "srp", lwsrp, 4) or bad
print(f"r582 publication plants: {'ESCAPE' if bad else 'all caught'}", flush=True)
sys.exit(1 if bad else 0)
