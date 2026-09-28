#!/usr/bin/env python3
"""Aggregate chunked mutants.py driver logs into campaign totals and K1-O8 coverage."""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / "tb" / "srp_top"))
import mutants  # committed arm table only
root = Path(sys.argv[2])
controls, arms = {}, {}
for log in sorted(root.glob("k*/driver.log")):
    for line in log.read_text().splitlines():
        m = re.match(r"control (\S+) (\S*): rc=(\d+) (PASS|FAIL)", line)
        if m: controls.setdefault((m[1], m[2]), set()).add(m[4])
        m = re.match(r"(\S+): rc=(\d+) failures=(\d+) (KILLED|UNPROVEN) tags=(.*)", line)
        if m: arms[m[1]] = (m[4], m[5])
        m = re.match(r"DRIVER_RC=(\d+)", line)
        if m and m[1] != "0": print("chunk nonzero:", log)
want = {m[0] for m in MUTANTS} if (MUTANTS := mutants.MUTANTS) else set()
covered = set()
for a, (v, tags) in arms.items():
    if v == "KILLED": covered |= set(tags.split(","))
fam = {f"{g}{i}" for g, n in [("K",12),("L",4),("M",12),("N",13),("O",8)] for i in range(1, n+1)}
print("controls:", sorted((k, sorted(v)) for k, v in controls.items()))
print(f"arms run {len(arms)}/{len(want)} killed {sum(v=='KILLED' for v,_ in arms.values())} "
      f"missing={sorted(want-set(arms))} unproven={sorted(a for a,(v,_) in arms.items() if v!='KILLED')}")
print(f"family coverage {len(fam & covered)}/{len(fam)} missing={sorted(fam-covered)}")
ok = all(v == {"PASS"} for v in controls.values()) and len(controls) == 7 and set(arms) == want \
     and all(v == "KILLED" for v, _ in arms.values()) and fam <= covered
print(f"equivalent driver tally: {len(controls)+len(want)+1} checks, all pass={ok}")
