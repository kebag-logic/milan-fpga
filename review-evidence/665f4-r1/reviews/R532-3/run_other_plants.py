#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Replay, through the lane's own campaign(), the SRP plants that live outside srp_mbx.cpp.

Usage: run_other_plants.py --repo <checkout at the head> --out <scratch dir>
"""
import argparse
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--repo", type=Path, required=True)
ap.add_argument("--out", type=Path, required=True)
a = ap.parse_args()
sys.path.insert(0, str(a.repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(a.repo / "sw/firmware/gtest"))
import srp_mutants  # noqa: E402

srp_mutants.DEFECTS = tuple(d for d in srp_mutants.DEFECTS
                            if d.path != "srp/srp_mbx.c" or d.suite != "srp_mbx.cpp" or d.debug)
print("plants:", len(srp_mutants.DEFECTS), flush=True)
failed = srp_mutants.campaign(a.out.resolve(), a.repo / "third_party/lwSRP", jobs=4)
print("ESCAPES" if failed else "ALL CAUGHT", flush=True)
raise SystemExit(1 if failed else 0)
