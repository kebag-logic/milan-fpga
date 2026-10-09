#!/usr/bin/env python3
"""Run the plant-table drift control and the two new table rows in the bank's app mode.

Usage: python3 -I table_probe.py --repo <clone> --packet <packet>
"""
import argparse, json, os, sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--repo", type=Path, required=True)
p.add_argument("--packet", type=Path, required=True)
a = p.parse_args()
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"; sys.dont_write_bytecode = True
os.environ["TMPDIR"] = str(a.packet.resolve() / "scratch")
sys.path.insert(0, str(a.repo.resolve() / "sw/firmware/ctrl/test"))
import aecp_mutants  # noqa: E402

aecp_mutants.controls()  # table drift: every test must be claimed by a row
print("plant-table controls PASS", flush=True)
names = ("nosub-bypasses-running-only", "nosub-bypasses-input-refusal")
rows = [d for d in aecp_mutants.DEFECTS if d.name in names]
assert len(rows) == 2
aecp_mutants.DEFECTS = rows  # campaign() re-runs controls(); restore the full table for that check
full = aecp_mutants.controls
aecp_mutants.controls = lambda: None
root = a.packet.resolve() / "scratch/table-campaign"
escaped = aecp_mutants.campaign(root, jobs=8)
aecp_mutants.controls = full
out = a.packet.resolve() / "receipts/table-campaign"
out.mkdir(parents=True, exist_ok=True)
for n in names:
    (out / f"{n}.log").write_bytes((root / f"{n}.log").read_bytes())
results = json.loads((root / "results.json").read_text())
(out / "results.json").write_text(json.dumps([{k: r[k] for k in ("name", "checks", "caught")} for r in results], indent=2) + "\n")
print("ESCAPED" if escaped else "both table rows caught in app mode at two interfaces", flush=True)
sys.exit(1 if escaped else 0)
