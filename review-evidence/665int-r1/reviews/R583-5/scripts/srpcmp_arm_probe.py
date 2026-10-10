#!/usr/bin/env python3
"""Reviewer probe (R583-5): the firmware gate's srpcmp arm against altered comparator reports.

usage: srpcmp_arm_probe.py REPO

Runs srp_wire_compare.py --self-test once for real, then feeds ctrl_arms.arm_srpcmp
altered copies of that JSON report through a stand-in for ctrl_arms.run (the arm's
code is unmodified) and prints each verdict against the expected one.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import ctrl_arms  # noqa: E402

real = ctrl_arms.run([sys.executable, "-I", "-B", str(ctrl_arms.SRP_COMPARE), "--self-test"])
assert real.returncode == 0, real.stderr
doc = json.loads(real.stdout)


def variant(fn):
    d = copy.deepcopy(doc)
    fn(d["controls"])
    return d


def drop_plant(c, name):
    c["plants"] = [p for p in c["plants"] if p["plant"] != name]


CASES = [
    ("the real report", lambda c: None, 0),
    ("one plant dropped (17 of 18)", lambda c: drop_plant(c, "oversized-frame"), 1),
    ("only one plant left", lambda c: c.__setitem__("plants", c["plants"][:1]), 1),
    ("a plant renamed", lambda c: c["plants"][0].__setitem__("plant", c["plants"][0]["plant"] + "-x"), 1),
    ("a control removed", lambda c: c.pop("packing_only"), 1),
    ("a control failing", lambda c: c.__setitem__("zero_padding", "FAIL"), 1),
    ("an extra plant added", lambda c: c["plants"].append(dict(c["plants"][0], plant="reviewer-extra")), 0),
    ("an extra control added", lambda c: c.__setitem__("reviewer_extra", "PASS"), 0),
    ("no plants", lambda c: c.__setitem__("plants", []), 1),
]
orig_run, bad = ctrl_arms.run, 0
for what, fn, want in CASES:
    out = json.dumps(variant(fn))
    ctrl_arms.run = lambda argv, **kw: subprocess.CompletedProcess(argv, 0, out, "")
    try:
        got = ctrl_arms.arm_srpcmp().rc
    finally:
        ctrl_arms.run = orig_run
    ok = got == want
    bad += not ok
    print(f"[{'ok' if ok else 'BAD'}] {what}: arm rc {got}, expected {want}")
print(f"srpcmp_arm_probe: {bad} unexpected verdict(s); real report: {len(doc['controls']['plants'])} plants")
sys.exit(1 if bad else 0)
