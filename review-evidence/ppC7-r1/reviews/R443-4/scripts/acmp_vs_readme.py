#!/usr/bin/env python3
"""Compare acmp_mutants.py pp_top arms' failing-check counts (each arm's log) with the README's "N of 43".

Usage: acmp_vs_readme.py <campaign-output-dir> <tb/pp_top/README.md> <campaign-log>
"""
import json, re, sys
from pathlib import Path
out, readme, log = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
verdict = {json.loads(l)["mutant"]: json.loads(l)["verdict"] for l in open(log) if l.startswith("{")}
rec, on = {}, False
for line in open(readme):
    if line.startswith("#"):
        on = "acmp_mutants.py" in line
    m = re.match(r"^\| `([a-z0-9_]+)` \|.*\| (\d+) of (\d+) \|\s*$", line)
    if on and m:
        rec[m.group(1)] = (int(m.group(2)), int(m.group(3)))
bad = 0
for arm, (n, tot) in rec.items():
    text = (out / f"{arm}@pp_top.log").read_text(errors="replace") if (out / f"{arm}@pp_top.log").exists() else ""
    got = sum(1 for l in text.splitlines() if re.match(r"^\s*FAIL\b", l))
    tally = re.findall(r"(\d+) checks: (\d+) PASS, (\d+) FAIL", text)
    ok = got == n and verdict.get(arm, verdict.get(arm + "@pp_top")) == "KILLED" and (not tally or int(tally[-1][0]) == tot)
    bad += not ok
    print(f"{'AGREE' if ok else 'DISAGREE'} {arm}: FAIL lines {got}, tally {tally[-1] if tally else None}, verdict {verdict.get(arm, verdict.get(arm + "@pp_top"))}; README {n} of {tot}")
print(f"README pp_top arms {len(rec)}, KILLED in run {sum(v == 'KILLED' for v in verdict.values())} of {sum(1 for k in verdict if not k.startswith('golden'))}, disagreeing {bad}")
sys.exit(1 if bad else 0)
