#!/usr/bin/env python3
"""R583-4: the SRP and AECP plants this PR adds, through their own campaigns.

Usage: python3 -I r583_4_srp_aecp_pr_plants.py <checkout> <base-test-dir> <lwsrp> <out-dir> <jobs>

A plant is this PR's when its name occurs in no base test script (dev 554e61d2).
SRP: every PR plant at two interfaces, then the round-5 TALKER_DECL plants at
one interface, as the gate runs them. AECP: the PR's plants through
aecp_mutants.campaign. One reviewer change, stated: aecp_mutants.controls (the
table-drift check that every AECP test is named by some plant) is answered
with nothing, because a filtered table names only the PR's tests.
"""
import re
import sys
from pathlib import Path

repo, base, lwsrp, out, jobs = (Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(),
                                Path(sys.argv[3]).resolve(), Path(sys.argv[4]).resolve(), int(sys.argv[5]))
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import aecp_mutants  # noqa: E402
import srp_mutants  # noqa: E402
import srp_pub_mutants  # noqa: E402

old = set(re.findall(r"""["']([A-Za-z0-9_.-]+)["']""", "\n".join(p.read_text() for p in base.glob("*.py"))))
srp_all = tuple(d for d in srp_mutants.DEFECTS if d.name not in old)
aecp_mutants.DEFECTS = tuple(d for d in aecp_mutants.DEFECTS if d.name not in old)
aecp_mutants.controls = lambda: None
print(f"SRP PR plants: {len(srp_all)}; AECP PR plants: {len(aecp_mutants.DEFECTS)}", flush=True)
srp_mutants.DEFECTS = srp_all
f2 = srp_mutants.campaign(out / "srp-if2", lwsrp, jobs, 2)
srp_mutants.DEFECTS = tuple(d for d in srp_all if d.name in srp_pub_mutants.ROUND5)
print(f"SRP round-5 plants at one interface: {len(srp_mutants.DEFECTS)}", flush=True)
f1 = srp_mutants.campaign(out / "srp-if1", lwsrp, jobs, 1)
fa = aecp_mutants.campaign(out / "aecp", jobs)
print(f"RESULT srp-if2 {'ESCAPE' if f2 else 'all caught'}; srp-if1 {'ESCAPE' if f1 else 'all caught'}; "
      f"aecp {'ESCAPE' if fa else 'all caught'}", flush=True)
sys.exit(1 if (f1 or f2 or fa) else 0)
