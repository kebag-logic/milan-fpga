#!/usr/bin/env python3
"""Require each masked identity bit to fail its own PV14 or PV15 row by name.

usage: check_walk.py PACKET/receipts/probes
"""
import re
import sys
from pathlib import Path

probes = Path(sys.argv[1])
killed, survivors, wrong = 0, [], []
for line in (probes / "summary-walk.tsv").read_text().splitlines():
    name, rc = line.split("\t")[:2]
    if rc == "rc=0":
        survivors.append(name)
        continue
    bit = int(name[-2:])
    fails = [x for x in (probes / (name + ".log")).read_text(errors="replace").splitlines()
             if x.startswith("FAIL: ")]
    if "msrp" in name:
        row = rf"PV14 two type (\d) StreamIDs that differ only in octet {7 - bit // 8}, bit {bit % 8}:"
        seen = {m.group(1) for m in (re.search(row, x) for x in fails) if m}
        good = seen == {"1", "2", "3"}
    else:
        good = any(f"PV15 VID 2 and the VID that differs only in bit {bit}:" in x for x in fails)
    killed += good
    if not good:
        wrong.append(name)
print(f"killed by their own row: {killed}; survivors: {survivors}; other: {wrong}")
