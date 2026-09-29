#!/usr/bin/env python3
"""Write MUTANTS.md from a d3_mutants.py results.json: every control, its suite, its
named checks, how many checks it failed, the first failing message, and whether the
count equals the suite README's mutation record. Usage: mutants_table.py results tree out
"""
import json
import re
import sys

results, tree, out = sys.argv[1:4]
records = json.load(open(results))
readme = {}
for rel in ("tb/pp_top/README.md", "tb/acmp_nvm/README.md"):
    for line in open(f"{tree}/{rel}"):
        m = re.match(r"\| `([A-Za-z0-9_]+)` \|.*\| (\d+) \|\s*$", line)
        if m:
            readme[m.group(1)] = int(m.group(2))
for line in open(f"{tree}/tb/rx_validator/README.md"):
    m = re.search(r"`(validator_admits_held_aecp)`.*\((\d+) FAILs\)", line)
    if m:
        readme[m.group(1)] = int(m.group(2))
rows = []
killed = 0
for r in records:
    if r["mutant"].startswith("golden-"):
        continue
    n = len(r["failing_checks"])
    killed += r["verdict"] == "KILLED"
    first = r["failing_checks"][0][:110].replace("|", "/") if n else ""
    rec = readme.get(r["mutant"])
    same = "yes" if rec == n else f"no ({rec})"
    names = ", ".join(f"`{c}`" for c in r["named_checks"])
    rows.append(f"| `{r['mutant']}` | `{r['suite']}` | {r['verdict']} | {names} | {n} | {same} | {first} |")
goldens = [r for r in records if r["mutant"].startswith("golden-")]
with open(out, "w") as f:
    f.write("# D3 mutation campaign at the head\n\n")
    f.write(f"`python3 tb/pp_top/d3_mutants.py` from a clean clone: {killed} of {len(rows)} KILLED; "
            f"goldens {', '.join(g['mutant'] + ' ' + g['verdict'] for g in goldens)}. KILLED means the "
            "build succeeded, the run completed with its tally, exited non-zero, and every named check "
            "failed. The count column is the number of failing checks; the README column says whether it "
            "equals the suite README's mutation record.\n\n")
    f.write("| Mutant | Suite | Verdict | Named checks (each failing) | Failing checks | = README | First failing message |\n")
    f.write("|---|---|---|---|---:|---|---|\n")
    f.write("\n".join(sorted(rows)) + "\n")
print(f"{killed} of {len(rows)} KILLED; {sum(1 for x in rows if '| yes |' in x)} README counts equal")
