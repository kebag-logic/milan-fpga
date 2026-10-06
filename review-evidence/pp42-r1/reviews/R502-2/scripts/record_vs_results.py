#!/usr/bin/env python3
"""Compare tb/pp_top/README.md's notify_mutants.py record (count and named
checks per row) with a results.json from notify_mutants.py. Usage: README RESULTS"""
import json, re, sys
readme, results = open(sys.argv[1]).read(), json.load(open(sys.argv[2]))
start = readme.index("### Mutation record: `notify_mutants.py`")
sec = readme[start:]
sec = sec[:sec.index("\n### ", 10)] if "\n### " in sec[10:] else sec
rows = {}
for line in sec.splitlines():
    m = re.match(r"^\| `([a-z0-9_]+)` \|.*\| (\d+)[:,] (.*) \|$", line)
    if m:
        rows[m.group(1)] = (int(m.group(2)), m.group(3))
bad = 0
for r in results:
    name = r["mutant"]
    if name.startswith("golden-"):
        continue
    if name not in rows:
        print("NO ROW", name); bad += 1; continue
    n, text = rows[name]
    got = len(r["failing_checks"])
    if got != n:
        print(f"COUNT {name}: record {n}, run {got}"); bad += 1
print(f"{len(rows)} record rows, {sum(1 for r in results if not r['mutant'].startswith('golden-'))} mutants, {bad} mismatches")
sys.exit(1 if bad else 0)
