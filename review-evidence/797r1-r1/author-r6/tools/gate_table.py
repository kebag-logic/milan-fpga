#!/usr/bin/env python3
"""Print the gate table from the runner summaries in a receipts gates directory.
Usage: gate_table.py <receipts/gates>"""
import json
import sys
from pathlib import Path

gates = Path(sys.argv[1])
ran, failed, skipped = [], 0, []
print("| Job | Step id | Name | rc | Last line |")
print("|---|---|---|---:|---|")
for job in ("wire-accountability", "docs-check-no-git", "docs-gates-0", "docs-gates-1", "docs-gates-2"):
    for line in (gates / f"{job}.summary.json").read_text(encoding="utf-8").splitlines():
        name, step, title, rc, why, _ = json.loads(line)
        if rc == "not run":
            skipped.append(f"{name}: {title}")
            continue
        log = gates / f"{name}__{step}.log"
        tail = gates / f"{name}__{step}.log.tail"
        text = (log if log.exists() else tail).read_text(encoding="utf-8", errors="replace").splitlines()
        last = next((t for t in reversed(text) if t.strip()), "")[:90].replace("|", "/")
        print(f"| {name} | {step} | {title[:58]} | {rc} | {last} |")
        ran.append(step)
        failed += rc != 0
print()
print(f"{len(ran)} steps ran, {failed} not rc 0, {len(skipped)} not run in these jobs.")
print()
print("Not run: " + "; ".join(skipped) + ".")
