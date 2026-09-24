#!/usr/bin/env python3
"""Compare the three mutation campaigns' verdict tables and per-leg check
tallies between two runs (base and head) recorded by run_campaign.sh.

usage: compare_campaigns.py <campaign-receipts-dir> [base-label head-label]
Exit 0 only if every verdict row and every tally line is identical.
"""
import json
import re
import sys
from pathlib import Path

TALLY = re.compile(r"^(?:\[build [^\]]*\] )?\d+ checks[:,].*$", re.M)


def rows(root: Path, label: str) -> dict[str, list[str]]:
    table: dict[str, list[str]] = {}
    desc = (root / f"{label}-desc.stdout").read_text().splitlines()
    table["desc verdict"] = [line for line in desc if not line.startswith("log:")]
    for log in sorted((root / f"{label}-desc").glob("*.log")):
        table[f"desc {log.name} tallies"] = TALLY.findall(log.read_text())
    table["srp verdict"] = (root / f"{label}-srp.stdout").read_text().splitlines()
    for log in sorted((root / f"{label}-srp").glob("*.log")):
        table[f"srp {log.name} tallies"] = TALLY.findall(log.read_text())
    results = json.loads((root / f"{label}-gsi" / "results.json").read_text())
    table["gsi verdict"] = [json.dumps(r, sort_keys=True) for r in results]
    table["gsi summary"] = (root / f"{label}-gsi.stdout").read_text().splitlines()[-1:]
    for log in sorted((root / f"{label}-gsi").glob("*-run.log")):
        table[f"gsi {log.name} tallies"] = TALLY.findall(log.read_text())
    return table


def main() -> int:
    root = Path(sys.argv[1])
    base, head = (sys.argv[2], sys.argv[3]) if len(sys.argv) > 3 else ("base", "head")
    a, b = rows(root, base), rows(root, head)
    ok = a.keys() == b.keys()
    for key in sorted(a.keys() | b.keys()):
        same = a.get(key) == b.get(key)
        ok &= same
        print(f"{'SAME' if same else 'DIFF'} {key}: {b.get(key)}")
        if not same:
            print(f"     {base}: {a.get(key)}")
    print(f"{len(a)} rows compared; identical={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
