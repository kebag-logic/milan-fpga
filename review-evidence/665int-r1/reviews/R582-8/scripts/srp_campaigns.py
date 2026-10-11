#!/usr/bin/env python3
"""The lwSRP-dependent plant campaigns of test_ctrl_firmware.py --self-test, run alone:
srp_mutants (publication plants included) at two interfaces, then the same
one-interface subset test_ctrl_firmware.py selects. Exit 1 when any plant escapes.

Usage: python3 srp_campaigns.py <candidate clone> <lwSRP checkout> <scratch out> [jobs]
"""
import sys
from pathlib import Path

clone, lwsrp, out = (Path(a).resolve() for a in sys.argv[1:4])
jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(clone / "sw/firmware/gtest"))
import srp_mutants  # noqa: E402
import srp_pub_mutants  # noqa: E402

print(f"SRP defects: {len(srp_mutants.DEFECTS)} (publication plants: "
      f"{sum(1 for d in srp_mutants.DEFECTS if d.name.startswith('pub-'))})", flush=True)
failed = srp_mutants.campaign(out / "srp-mutants", lwsrp, jobs)
complete = srp_mutants.DEFECTS
srp_mutants.DEFECTS = tuple(d for d in complete
                            if d.name.startswith(("four-way-", "binding-", "feedback-", "r10-",
                                                  "p11-", "srp-bound-", "srp-term-",
                                                  "srp-poll-extra", "srp-send-extra",
                                                  *srp_pub_mutants.ROUND5)))
print(f"SRP one-interface subset: {len(srp_mutants.DEFECTS)}", flush=True)
failed = srp_mutants.campaign(out / "srp-if1-mutants", lwsrp, jobs, 1) or failed
print(f"srp campaigns: {'FAIL' if failed else 'PASS'}", flush=True)
sys.exit(1 if failed else 0)
