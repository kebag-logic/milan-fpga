#!/usr/bin/env python3
"""[R316] Tabulate the probe receipts: python3 matrix.py <receipts dir>."""
import json
import sys
from pathlib import Path

d = Path(sys.argv[1])
runs = ["probe-base-sdk", "probe-head-sdk", "probe-head-sdk-disabled",
        "probe-base-absent", "probe-head-absent", "probe-head-absent-disabled"]
data = {r: {x["id"]: x for x in json.loads((d / f"{r}.json").read_text())["results"]}
        for r in runs}
labels = {i: x["label"] for i, x in data["probe-head-sdk"].items()}


def cell(text: str) -> str:
    return text.replace("|", "\\|")


def verdict(run: str, cid: str) -> str:
    row = data[run][cid]
    if row["verdict"] == "ACCEPTED":
        return "ACCEPTED"
    reason = row["reason"]
    if "single-store rule" in reason:
        return "REFUSED single-store"
    if "macro replacement rule" in reason:
        return "REFUSED macro-replacement"
    return "REFUSED other: " + reason[:60]


print("| id | variant | " + " | ".join(r.replace("probe-", "") for r in runs) + " |")
print("|---|---|" + "---|" * len(runs))
for cid in sorted(labels):
    print(f"| {cid} | {cell(labels[cid])} | " +
          " | ".join(cell(verdict(r, cid)) for r in runs) + " |")
