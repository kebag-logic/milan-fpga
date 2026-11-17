#!/usr/bin/env python3
"""Reviewer spot-check: plant named defects of the head's own SRP table (srp_mutants.DEFECTS) and require each caught.

usage: table_plants.py CLONE OUT INTERFACES ENTITY NAME...
  ENTITY '-' for the campaign's default entity. Each defect is planted in a disposable copy under OUT by
  srp_mutants.campaign, which prints [ok] or [ESCAPED] per defect; the clone is not written.
"""
import sys
from pathlib import Path

clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
interfaces, entity, names = int(sys.argv[3]), sys.argv[4], sys.argv[5:]
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))
import srp_mutants  # noqa: E402

table = {d.name: d for d in srp_mutants.DEFECTS}
missing = [n for n in names if n not in table]
if missing:
    print("not in the table:", missing)
    sys.exit(2)
srp_mutants.DEFECTS = tuple(table[n] for n in names)
failed = srp_mutants.campaign(out, clone / "third_party/lwSRP", 2, interfaces, "" if entity == "-" else entity)
print("RESULT:", "FAIL" if failed else "PASS")
sys.exit(1 if failed else 0)
