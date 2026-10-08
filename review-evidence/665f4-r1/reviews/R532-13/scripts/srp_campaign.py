"""R532-13: the standing SRP mutation campaign exactly as test_ctrl_firmware.py --self-test
selects it: the full table at IF=2, the prefixed subset at IF=1. Usage: <repo> <lwsrp> <out> <ifcount>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, LWSRP, OUT
import srp_mutants
n = int(sys.argv[4])
if n == 1:
    srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS if d.name.startswith((
        "four-way-", "binding-", "feedback-", "r10-", "p11-", "srp-bound-", "srp-term-",
        "srp-poll-extra", "srp-send-extra")))
print(f"{len(srp_mutants.DEFECTS)} SRP plants at IF={n}", flush=True)
failed = srp_mutants.campaign(OUT / f"campaign-if{n}", LWSRP, 4, n)
print(f"SRP campaign IF={n}: {'FAIL' if failed else 'PASS'}")
sys.exit(1 if failed else 0)
