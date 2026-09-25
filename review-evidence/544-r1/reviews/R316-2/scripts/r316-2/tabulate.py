#!/usr/bin/env python3
"""[R316] R316-2 tabulator: python3 tabulate.py <receipts dir> <prefix> <run>...

Prints one Markdown row per case: the verdict of each named run, with the
refusal classified by the rule sentence it carries."""
import json
import sys
from pathlib import Path

d, prefix, runs = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
data = {r: {x["id"]: x for x in json.loads((d / f"{prefix}-{r}.json").read_text())["results"]}
        for r in runs}


def verdict(row: dict) -> str:
    if row["verdict"] == "ACCEPTED":
        return "ACCEPTED"
    reason = row["reason"]
    if "identity-sample absence rule" in reason:
        for key, name in (("no asm", "asm"), ("outside the two", "shape"),
                          ("nested functions", "nested"), ("storage class", "storage"),
                          ("never escape", "escape")):
            if key in reason:
                return f"REFUSED absence rule ({name})"
        return "REFUSED absence rule"
    if "macro replacement rule" in reason:
        return "REFUSED macro replacement rule"
    return "REFUSED other: " + reason[:70].replace("|", "\\|")


first = data[runs[0]]
print("| id | case | " + " | ".join(runs) + " |")
print("|---|---|" + "---|" * len(runs))
for cid, row in first.items():
    print(f"| {cid} | {row['label'].replace('|', chr(92) + '|')} | "
          + " | ".join(verdict(data[r][cid]) for r in runs) + " |")
