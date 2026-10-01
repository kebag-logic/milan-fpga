#!/usr/bin/env python3
"""Summarise an acmp_mutants.py results.json: verdict, failing count and tally per record."""
import json, re, sys
from pathlib import Path
out = Path(sys.argv[1])
TALLY = re.compile(r"(\d+) checks: \d+ PASS, (\d+) FAIL|\] (\d+) checks, (\d+) failures")
for r in json.loads((out / "results.json").read_text()):
    log = (out / f"{r['mutant']}.log").read_text(errors="replace")
    t = TALLY.findall(log)
    last = t[-1] if t else None
    tot = (last[0] or last[2]) if last else "?"
    nf = (last[1] or last[3]) if last else "?"
    print(f"{r['mutant']:42s} {r['verdict']:8s} {nf} of {tot}  named={r.get('named_checks')}")
