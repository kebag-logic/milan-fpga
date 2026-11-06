#!/usr/bin/env python3
"""The ruling's bar, read from the scripts and the campaign receipts rather than restated.

usage: ruling848.py <final script> <base script> <f5ccb318 script> <212b7d6e script> <work dir> <r787 packet receipt> <r788 packet receipt> <r787 final receipt> <r788 final receipt>
"""
import re, subprocess, sys
from pathlib import Path

final, base, first, prior, work = map(Path, sys.argv[1:6])
p787, p788, f787, f788 = map(Path, sys.argv[6:10])
SRC = 'f"| {cell(source_of(finding))} | {cell(finding.correction)} |")'
PLANTS = {
    "R1 (F1)": (SRC, 'f"| {cell(finding.source)} | {cell(finding.correction)} |")'),
    "O1 (F2)": ('for p in pages if p.area == area]', 'for p in pages if p.area == area and p.path != OUTPUT]'),
    "W7 (F3)": ('grouped.setdefault(lanes[finding.page], []).append((finding, line))', 'grouped.setdefault(lanes[finding.page], [(finding, line)])'),
    "W8 (F3)": ('f"- Statement: {finding.quote}", ', ''),
}
print("| Mutant | base | f5ccb318 | 212b7d6e | final |\n|---|---|---|---|---|")
for name, (old, new) in PLANTS.items():
    cells = []
    for label, script in (("base", base), ("first", first), ("prior", prior), ("final", final)):
        text = script.read_text(encoding="utf-8")
        if text.count(old) != 1:
            cells.append(f"n/a ({text.count(old)} targets)")
            continue
        target = work / f"{label}-{name[:2]}" / "scripts" / "docs_inventory.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text.replace(old, new), encoding="utf-8")
        done = subprocess.run([sys.executable, "-I", str(target), "--selftest"], capture_output=True, text=True, timeout=120)
        cells.append("killed" if done.returncode else "SURVIVED")
    print(f"| {name} | " + " | ".join(cells) + " |")

print("\nR787 survivors at 212b7d6e, from its receipt, against the final head:")
def r787(path):
    rows = {}
    for line in path.read_text().splitlines():
        parts = [c.strip() for c in line.split("|")]
        if len(parts) >= 4 and not line.startswith("#"):
            rows[parts[0]] = (parts[1], parts[3])
    return rows
was, now = r787(p787), r787(f787)
left = 0
for ident, (verdict, what) in was.items():
    if verdict == "SURVIVED":
        print(f"  {ident}: {now[ident][0]} :: {what}")
        left += now[ident][0] == "SURVIVED"
print(f"  still surviving: {left}")

print("\nR788 survivors at 212b7d6e, from its receipt, against the final head:")
def r788(path):
    rows, name = {}, None
    for line in path.read_text().splitlines():
        if line.startswith("   head: "):
            rows[name] = line[9:].split()[0]
        elif not line.startswith("   "):
            name = line
    return rows
was, now = r788(p788), r788(f788)
left = 0
for name, verdict in was.items():
    if verdict == "SURVIVED":
        print(f"  {now.get(name)} :: {name}")
        left += now.get(name) == "SURVIVED"
print(f"  still surviving: {left}")
