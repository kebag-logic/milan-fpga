#!/usr/bin/env python3
"""Tabulate probe JSON results side by side: tools/table.py col=file.json ..."""
import json, sys
cols = [a.split("=", 1) for a in sys.argv[1:]]
data = [(name, {r["label"]: r for r in json.load(open(path))["results"]}) for name, path in cols]
labels = list(data[0][1])
for label in labels:
    cells = []
    for name, rows in data:
        r = rows.get(label)
        if r is None:
            cells.append("-")
        elif r["verdict"] == "ACCEPTED":
            cells.append("ACCEPTED")
        else:
            why = r["reason"]
            cells.append("REFUSED: " + why[:110].replace("\n", " "))
    print(label)
    for (name, _), cell in zip(data, cells):
        print(f"    {name:10s} {cell}")
