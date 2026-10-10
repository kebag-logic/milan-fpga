#!/usr/bin/env python3
"""r582_srp_campaign.py - R582-3: the firmware gate's SRP plant campaigns, run apart to save wall time.

Usage: r582_srp_campaign.py <checkout> <lwsrp> <scratch-root>

Replicates test_ctrl_firmware.py's --self-test tail (its lines 202-217): the
full SRP table at two interfaces, the one-interface subset, and the lwSRP pin
arms, with the gate's own functions. Read-only on <checkout>.
"""
import sys
from pathlib import Path

checkout, lwsrp, root = (Path(a).resolve() for a in sys.argv[1:4])
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(checkout / "sw/firmware/gtest"))
import ctrl_mutants  # noqa: E402
import srp_mutants  # noqa: E402

print(f"SRP table: {len(srp_mutants.DEFECTS)} defects at two interfaces", flush=True)
failed = srp_mutants.campaign(root / "srp-mutants", lwsrp, 4)
complete = srp_mutants.DEFECTS
srp_mutants.DEFECTS = tuple(d for d in complete if d.name.startswith(
    ("four-way-", "binding-", "feedback-", "r10-", "p11-", "srp-bound-", "srp-term-", "srp-poll-extra",
     "srp-send-extra")))
print(f"SRP one-interface subset: {len(srp_mutants.DEFECTS)} defects", flush=True)
failed = srp_mutants.campaign(root / "srp-if1-mutants", lwsrp, 4, 1) or failed
srp_mutants.DEFECTS = complete
failed = ctrl_mutants.lwsrp_pin_arms(root / "mutants", lwsrp) != 0 or failed
print(f"r582 SRP campaigns: {'FAIL' if failed else 'PASS'}", flush=True)
sys.exit(1 if failed else 0)
