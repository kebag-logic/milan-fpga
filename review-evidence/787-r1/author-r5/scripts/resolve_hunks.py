#!/usr/bin/env python3
"""Resolve the conflict hunks of one file by an explicit per-hunk order.

usage: resolve_hunks.py FILE ORDER [ORDER ...]
ORDER per hunk, in file order: ours | theirs | ours+theirs | theirs+ours,
optionally suffixed with ':blank' to put one empty line between the sides.
Refuses unless the file has exactly as many hunks as orders and no nested
or diff3 markers.
"""
import sys
from pathlib import Path

path = Path(sys.argv[1])
orders = sys.argv[2:]
lines = path.read_text(encoding="utf-8").split("\n")
out, hunks, i = [], 0, 0
while i < len(lines):
    line = lines[i]
    if line.startswith("<<<<<<< "):
        ours, theirs, j = [], [], i + 1
        while not lines[j].startswith("======="):
            if lines[j].startswith(("<<<<<<<", "|||||||", ">>>>>>>")):
                sys.exit(f"{path}: unexpected marker at line {j + 1}")
            ours.append(lines[j]); j += 1
        j += 1
        while not lines[j].startswith(">>>>>>> "):
            if lines[j].startswith(("<<<<<<<", "|||||||", "=======")):
                sys.exit(f"{path}: unexpected marker at line {j + 1}")
            theirs.append(lines[j]); j += 1
        if hunks >= len(orders):
            sys.exit(f"{path}: more hunks than orders")
        order, _, sep = orders[hunks].partition(":")
        sides = {"ours": ours, "theirs": theirs}
        parts = [sides[name] for name in order.split("+")]
        for k, part in enumerate(parts):
            if k and sep == "blank":
                out.append("")
            out.extend(part)
        hunks += 1
        i = j + 1
        continue
    out.append(line)
    i += 1
if hunks != len(orders):
    sys.exit(f"{path}: {hunks} hunks, {len(orders)} orders")
path.write_text("\n".join(out), encoding="utf-8")
print(f"{path}: {hunks} hunks resolved: {' '.join(orders)}")
