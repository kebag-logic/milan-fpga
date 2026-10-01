#!/usr/bin/env python3
"""R410-3: tabulate the three acmp_mutants.py groups (verdict, rc, failing of total)."""
import json, re, sys
from pathlib import Path
R = Path(sys.argv[1])
TALLY = re.compile(r"^(?:ACMP: (\d+) checks, (\d+) failures|(\d+) checks: \d+ PASS, (\d+) FAIL)$", re.M)
n = k = 0
for g in "ABC":
    for r in json.loads((R / f"acmp_mutants_{g}" / "results.json").read_text()):
        t = TALLY.findall((R / f"acmp_mutants_{g}" / f"{r['mutant']}.log").read_text(errors="replace"))
        tot, fl = ((t[-1][0] or t[-1][2]), (t[-1][1] or t[-1][3])) if t else ("?", "?")
        print(f"{g} {r['mutant']:40s} {r['verdict']:8s} build={r.get('build_rc')} run={r.get('run_rc')} "
              f"fail {fl} of {tot} missing={r.get('missing')}")
        if not r["mutant"].startswith("golden-"):
            n += 1; k += r["verdict"] == "KILLED"
print(f"mutant records: {k} of {n} KILLED (19 distinct mutant/suite records)")
