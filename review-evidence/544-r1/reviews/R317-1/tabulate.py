#!/usr/bin/env python3
"""Tabulate probe JSON results side by side (R317-1). Usage: tabulate.py DIR TAG..."""
import json, sys
from pathlib import Path
d = Path(sys.argv[1]); tags = sys.argv[2:]
data = {t: {r["label"]: r for r in json.loads((d / f"{t}.json").read_text())["rows"]} for t in tags}
labels = list(data[tags[0]])
short = lambda r: "ACC" if r["verdict"] == "ACCEPTED" else "REF:" + (
    "SAMPLE" if "single-store" in r["reason"] else "MACRO" if "macro replacement rule" in r["reason"]
    else "TEXT-ID" if "consume the unmodified" in r["reason"] else "other")
print("| case | " + " | ".join(tags) + " |")
print("|---" * (len(tags) + 1) + "|")
for l in labels:
    print(f"| {l} | " + " | ".join(short(data[t][l]) if l in data[t] else "-" for t in tags) + " |")
