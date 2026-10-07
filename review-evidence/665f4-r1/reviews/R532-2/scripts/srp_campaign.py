#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Run the lane's own SRP planted-defect campaign (srp_mutants.DEFECTS) at
the checkout's head into a scratch root. usage: srp_campaign.py REPO OUT"""
import sys
from pathlib import Path
repo=Path(sys.argv[1]).resolve()
sys.path[:0]=[str(repo/"sw/firmware/ctrl/test"),str(repo/"sw/firmware/gtest")]
import srp_mutants
print("defects:",len(srp_mutants.DEFECTS),flush=True)
raise SystemExit(int(srp_mutants.campaign(Path(sys.argv[2]),repo/"third_party/lwSRP",4)))
