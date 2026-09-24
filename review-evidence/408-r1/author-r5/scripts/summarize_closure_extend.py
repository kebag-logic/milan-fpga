#!/usr/bin/env python3
"""[A261] scratch: split R273-6 closure_extend.py's raw "HOLE" count the way
its own receipt summary did: GCC refuses while the reader reads names, the
reader refuses while GCC reads names (fail-closed), or both read names and
differ (a real hole). Reads the unchanged probe's JSONL output only."""
import collections
import json
import sys

tally = collections.Counter()
holes = []
part_a = collections.Counter()
for line in open(sys.argv[1], encoding="utf-8"):
    row = json.loads(line)
    part, kind = row["part"], row["kind"]
    if kind == "HOLE":
        gcc, reader = row["gcc"], row["reader"]
        if gcc is None:
            kind = "GCC refuses to preprocess, reader reads names"
        elif reader is None:
            kind = "reader refuses, GCC reads (fail-closed)"
        else:
            kind = "BOTH READ NAMES AND DIFFER"
        holes.append((part, kind, row["label"], reader, gcc))
    elif kind == "agree" and row["gcc"] is None:
        kind = "agree(both refuse)"
    tally[(part, kind)] += 1
    if part == "A":
        part_a["cells"] += 1
        part_a["record_vs_gcc mismatches"] += not row["record_vs_gcc"]
        part_a["closes"] += row["kind"].endswith("+closes")
        part_a["negative control among closes"] += (
            row["label"] == "U+00B7 inside a directive name"
            and row["kind"].endswith("+closes"))
for key in sorted(tally):
    print(f"  {key[0]} {key[1]}: {tally[key]}")
print("Part A:", dict(part_a))
print("cells whose raw kind is HOLE:")
for part, kind, label, reader, gcc in holes:
    print(f"  {part} {kind}: {label} (reader {reader}, gcc {gcc})")
