#!/usr/bin/env python3
"""The gate table, from the run's own log and rc files. Usage: gate_table.py <logs> <workflow>"""
import re, sys
from pathlib import Path
import yaml
logs, flow = Path(sys.argv[1]), yaml.safe_load(open(sys.argv[2]))
print("| Job | Step id | Name | rc | Last line |")
print("|---|---|---|---:|---|")
counts = {"run": 0, "bad": 0, "off": 0}
off = []
for job, spec in flow["jobs"].items():
    for i, st in enumerate(spec.get("steps", [])):
        if "run" not in st:
            continue
        ident = st.get("id", f"step{i}")
        stem = logs / f"{job}__{ident}"
        rc_file = stem.with_suffix(".rc")
        name = st.get("name", "")[:58]
        if rc_file.is_file():
            rc = rc_file.read_text().strip()
            lines = [l for l in stem.with_suffix(".log").read_text(errors="replace").splitlines() if l.strip()]
            last = re.sub(r"[|`]", " ", lines[-1])[:90] if lines else ""
            last = re.sub(r"$VALIDATION_STORAGE/797-a711b/gates2?/wt", "<clone>", last)
            print(f"| {job} | {ident} | {name} | {rc} | {last} |")
            counts["run"] += 1
            counts["bad"] += rc != "0"
        else:
            counts["off"] += 1
            off.append(f"{job}: {name}")
print()
print(f"{counts['run']} steps ran, {counts['bad']} not rc 0, {counts['off']} not run.")
print()
print("Not run: " + "; ".join(off) + ".")
