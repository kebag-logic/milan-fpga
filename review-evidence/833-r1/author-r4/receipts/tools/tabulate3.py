#!/usr/bin/env python3
"""usage: tabulate3.py MATRIX_JSON  (prints the per-control Markdown table and each red's failing words)"""
import json, re, sys
rows = json.load(open(sys.argv[1]))
controls = list(dict.fromkeys(r["control"] for r in rows))
mutants = list(dict.fromkeys(r["mutant"] for r in rows))
cell = {(r["mutant"], r["control"]): r for r in rows}
short = [c.removeprefix("owner_") for c in controls]
print("| Mutant | " + " | ".join(short) + " | red |")
print("|---|" + "---|" * len(short) + "---:|")
for m in mutants:
    cs = [cell[(m, c)] for c in controls]
    print(f"| {m} | " + " | ".join("ok" if r["rc"] == 0 else f"RED({r['rc']})" for r in cs)
          + f" | {sum(r['rc'] != 0 for r in cs)} |")
print("\nFailing words:")
for m in mutants:
    for c in controls:
        r = cell[(m, c)]
        if r["rc"]:
            words = re.sub(r"^owner_\w+ FAIL [\d.]+s ", "", r["last"])
            print(f"- {m} / {c.removeprefix('owner_')} ({r['seconds']} s): {words[:160]}")
