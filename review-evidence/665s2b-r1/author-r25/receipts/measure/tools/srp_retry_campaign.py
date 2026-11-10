#!/usr/bin/env python3
"""Scratch: run only srp_retry_mutants' defects through srp_mutants.campaign's planting, at both interface counts.
usage: srp_retry_campaign.py CHECKOUT OUT"""
import sys
from pathlib import Path
ck, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ck / "sw/firmware/ctrl/test")); sys.path.insert(0, str(ck / "sw/firmware/gtest"))
import srp_mutants, srp_retry_mutants
srp_mutants.DEFECTS = srp_retry_mutants.defects(srp_mutants.Defect)
bad = False
for i in (1, 2):
    bad |= srp_mutants.campaign(out / f"if{i}", (ck / "third_party/lwSRP").resolve(), 4, i)
sys.exit(int(bad))
