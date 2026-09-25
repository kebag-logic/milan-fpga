#!/usr/bin/env python3
"""Tabulate probe JSON side by side (R317-2). Usage: tabulate2.py DIR TAG...
Reason classes: SAMPLE = identity-sample absence rule (head) or single-store
rule (round-1 head), MACRO = identity-sample macro replacement rule,
TEXT-ID = pre-existing source-text identity rule, other = any other refusal."""
import json, sys
from pathlib import Path
d = Path(sys.argv[1]); tags = sys.argv[2:]
data = {t: {r["label"]: r for r in json.loads((d / f"{t}.json").read_text())["rows"]} for t in tags}
labels = list(data[tags[0]])
def short(r):
    if r["verdict"] == "ACCEPTED":
        return "ACC"
    s = r["reason"]
    return "REF:" + ("SAMPLE" if ("identity-sample absence rule" in s or "single-store" in s)
                     else "MACRO" if "macro replacement rule" in s
                     else "TEXT-ID" if "consume the unmodified" in s else "other")
print("| case | " + " | ".join(tags) + " |")
print("|---" * (len(tags) + 1) + "|")
for l in labels:
    print(f"| {l} | " + " | ".join(short(data[t][l]) if l in data[t] else "-" for t in tags) + " |")
