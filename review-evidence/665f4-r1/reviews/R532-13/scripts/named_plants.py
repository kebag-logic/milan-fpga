"""R532-13: the three round-13 named plants, through the standing campaign driver, at IF=1 and IF=2.
Usage: python3 -I named_plants.py <repo> <lwsrp> <out> <ifcount>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, LWSRP, OUT
import srp_mutants
n = int(sys.argv[4])
names = ("feedback-leave-clears-advertise-only", "feedback-failed-indication-as-advertise",
         "feedback-change-clears-both-kinds")
full = srp_mutants.DEFECTS
srp_mutants.DEFECTS = tuple(d for d in full if d.name in names)
assert len(srp_mutants.DEFECTS) == 3, srp_mutants.DEFECTS
failed = srp_mutants.campaign(OUT / f"named-if{n}", LWSRP, 4, n)
print(f"named plants IF={n}: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
