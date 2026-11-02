#!/usr/bin/env python3
"""usage: tabulate.py LOG... > table.md

Read the `--mutants --matrix` driver lines ("NAME / TARGET: verdict rc N S s: last")
from every LOG (later logs win) and print one Markdown row per mutant, with a
column per control and the whole test, then each red's failing words."""
import re, sys

LINE = re.compile(r"^(?P<m>[\w.-]+) / (?P<t>\w+): (?P<v>red|green|cut) rc (?P<rc>\S+) (?P<s>[\d.]+) s: (?P<last>.*)$")
cells, mutants, targets = {}, [], []
for path in sys.argv[1:]:
    for line in open(path, errors="replace"):
        hit = LINE.match(line.rstrip("\n"))
        if not hit:
            continue
        m, t = hit["m"], hit["t"]
        if m not in mutants:
            mutants.append(m)
        if t not in targets:
            targets.append(t)
        cells[(m, t)] = hit
order = [t for t in targets if t != "whole"] + ["whole"]
short = [t.removeprefix("owner_") for t in order]
print("| Mutant | " + " | ".join(short) + " | red |")
print("|---|" + "---|" * len(order) + "---:|")
for m in mutants:
    row = []
    for t in order:
        c = cells.get((m, t))
        row.append("-" if c is None else "ok" if c["v"] == "green" else ("CUT" if c["v"] == "cut" else f"RED({c['rc']})"))
    print(f"| {m} | " + " | ".join(row) + f" | {sum(r.startswith(('RED', 'CUT')) for r in row)} |")
print("\nFailing words:")
for m in mutants:
    for t in order:
        c = cells.get((m, t))
        if c is not None and c["v"] != "green":
            words = re.sub(r"^\w+ FAIL [\d.]+s ", "", c["last"])
            print(f"- {m} / {t.removeprefix('owner_')} ({c['s']} s): {words[:170]}")
