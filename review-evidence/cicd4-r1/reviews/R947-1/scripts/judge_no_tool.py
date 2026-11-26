#!/usr/bin/env python3
"""Show whether the census judge's inventory needs Yosys or sv2v: any subprocess that names either fails.
Usage (from sw/mailbox of the checkout): python3 judge_no_tool.py"""
import os
import subprocess
import sys

sys.path.insert(0, os.getcwd())
real = subprocess.Popen.__init__
seen = []


def guarded(self, args, *a, **k):
    text = " ".join(map(str, args)) if isinstance(args, (list, tuple)) else str(args)
    seen.append(text[:160])
    if "yosys" in text.split("/")[-1] or "sv2v" in text:
        raise FileNotFoundError("probe: EDA tool invoked: " + text[:160])
    return real(self, args, *a, **k)


subprocess.Popen.__init__ = guarded
import census_legs as c  # noqa: E402
import census_selftest as s  # noqa: E402
from census_rules import RULES  # noqa: E402

inv = c.inventory()
print("arms", len(c.names(inv)), "groups", len(inv))
print("enforced == RULES", s.enforced() == set(RULES), len(RULES))
print("subprocesses:", seen)
