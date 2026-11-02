#!/usr/bin/env python3
"""Tabulate run_control.py results: tabulate.py RECEIPT_DIR"""
import sys, pathlib
R = pathlib.Path(sys.argv[1])
ctrls = ["owner_report","owner_reparented","owner_late_exit","owner_stall","owner_shell_window","owner_survivor","owner_vanishing"]
muts = sorted({p.name.split("__")[0] for p in R.glob("*.rc")}, key=lambda m: (m!="none", m))
print("mutant".ljust(26), " ".join(c.replace("owner_","")[:9].ljust(9) for c in ctrls), " red")
for m in muts:
    row=[]; red=0
    for c in ctrls:
        rc = (R/f"{m}__{c}.rc").read_text().strip()
        row.append(("ok" if rc=="0" else f"RED({rc})").ljust(9)); red += rc!="0"
    print(m.ljust(26), " ".join(row), f" {red}")
print()
for m in muts:
    for c in ctrls:
        if (R/f"{m}__{c}.rc").read_text().strip()!="0":
            last=[l for l in (R/f"{m}__{c}.log").read_text().splitlines() if " FAIL " in l]
            print(f"{m} / {c}: {last[-1][:300] if last else '(no FAIL line: killed by the 150 s bound)'}")
