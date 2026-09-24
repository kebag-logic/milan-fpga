#!/usr/bin/env python3
"""Tabulate probe receipts: one row per case, one column per run."""
import json
import sys
from pathlib import Path

def main():
    runs = sys.argv[1:]
    data = {r: {x["label"]: x for x in json.loads(Path(r).read_text())["results"]} for r in runs}
    print("| case | " + " | ".join(Path(r).stem for r in runs) + " |")
    print("|---" * (len(runs) + 1) + "|")
    for label in data[runs[0]]:
        cells = []
        for r in runs:
            x = data[r][label]
            cells.append(x["verdict"] + ("" if x["verdict"] == "ACCEPTED" else ": " + x["reason"][:90].replace("|", "/").replace("\n", " ")))
        print(f"| {label} | " + " | ".join(cells) + " |")

if __name__ == "__main__":
    main()
