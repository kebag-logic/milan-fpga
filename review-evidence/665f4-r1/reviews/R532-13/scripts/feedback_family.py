"""R532-13: every standing SrpFeedback-named plant (the file this round edits), through the
standing campaign driver at one interface count. Usage: <repo> <lwsrp> <out> <ifcount>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, LWSRP, OUT
import srp_mutants
n = int(sys.argv[4])
srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.test.startswith("SrpFeedback."))
print(f"{len(srp_mutants.DEFECTS)} SrpFeedback plants", flush=True)
failed = srp_mutants.campaign(OUT / f"family-if{n}", LWSRP, 4, n)
print(f"SrpFeedback family IF={n}: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
