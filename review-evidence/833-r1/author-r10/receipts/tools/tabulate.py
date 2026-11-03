#!/usr/bin/env python3
"""Tabulate --matrix logs: one row per mutant, one column per owner control and the whole test.

usage: python3 -I -B tabulate.py <tree> LOG...
Prints a markdown table, then the failing words of each mutant's named control.
"""
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / "scripts"))
import process_test_support as pts  # noqa: E402
import test_suite_cancellation as tsc  # noqa: E402

cells, lines = {}, {}
for log in sys.argv[2:]:
    for line in Path(log).read_text().splitlines():
        found = re.match(r"(\S+) / (\S+): (red|green|cut) rc \S+ ([0-9.]+) s: (.*)", line)
        if found:
            name, target, verdict, _seconds, last = found.groups()
            cells[(name, target)] = verdict
            lines[(name, target)] = last
targets = [*tsc.OWNER_CONTROLS, "whole"]
short = [t.removeprefix("owner_") for t in targets]
print("| Mutant | " + " | ".join(short) + " | red |")
print("|---|" + "---|" * len(targets) + "---:|")
for name in pts.MUTANTS:
    row = []
    for target in targets:
        verdict = cells.get((name, target), "missing")
        row.append({"green": "ok", "red": "RED", "cut": "CUT"}.get(verdict, verdict))
    print(f"| {name} | " + " | ".join(row) + f" | {sum(v != 'ok' for v in row)} |")
print()
bad = []
for name, (control, words, *_edits) in pts.MUTANTS.items():
    if name == "none":
        bad += [f"none / {t}: {cells.get((name, t))}" for t in targets if cells.get((name, t)) != "green"]
    elif control:
        ok = cells.get((name, control)) == "red" and words in lines.get((name, control), "")
        print(f"- {name} / {control.removeprefix('owner_')}: {lines.get((name, control), '')[:160]}")
        if cells.get((name, "whole")) == "green":
            print(f"  (green on whole)")
    else:
        reds = [t for t in targets if cells.get((name, t)) != "green"]
        print(f"- {name}: no control; red on {reds or 'nothing'}")
print("\nproblems:", bad or "none")
