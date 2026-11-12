#!/usr/bin/env python3
"""Plant chosen defects of a checkout's SRP or control campaign and require each caught (lane 895 helper).

usage: run_defects.py CHECKOUT OUT srp IF NAME[,NAME...]   (srp_mutants.campaign at IF interfaces)
       run_defects.py CHECKOUT OUT control NAME[,NAME...]  (ctrl_mutants.campaign)
"""
import sys
from pathlib import Path
checkout = Path(sys.argv[1]).resolve(); out = Path(sys.argv[2]).resolve(); kind = sys.argv[3]
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test")); sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
if kind == "srp":
    import srp_mutants
    n_if = int(sys.argv[4]); names = sys.argv[5].split(",")
    srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name in names or any(
        n.endswith("*") and d.name.startswith(n[:-1]) for n in names))
    print("planting", len(srp_mutants.DEFECTS), "SRP defects at", n_if, "interface(s)", flush=True)
    failed = srp_mutants.campaign(out, (checkout / "third_party/lwSRP").resolve(), 4, n_if)
else:
    import ctrl_mutants
    from ctrl_reuse import cut_reuse
    names = sys.argv[4].split(",")
    print("unnamed tests in the whole table:", ctrl_mutants.unnamed_tests(), flush=True)
    ctrl_mutants.MUTANTS = tuple(m for m in ctrl_mutants.MUTANTS if m.name in names)
    ctrl_mutants.unnamed_tests = lambda: []  # the whole table's rule is checked above; this run plants a subset
    print("planting", len(ctrl_mutants.MUTANTS), "control mutants", flush=True)
    cut_reuse(out / "reuse")
    failed = ctrl_mutants.campaign(out / "mutants", out / "reuse", 4, (1, 1), None)
print("RESULT", "FAIL" if failed else "PASS")
sys.exit(1 if failed else 0)
