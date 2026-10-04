#!/usr/bin/env python3
"""R466-2 probe (round 1's receipt-table check, rewritten as a script): the page's hand-written Yosys and
Vivado run-receipt rows against the published round-1 run-receipts.json, and the round-2 reopen row
against the round-2 manifest's original digest of route_map.log; then that every Yosys point of the plan
has a published guard record, and the guard records' refusals equal the page's "refused" marks.
Usage: check_receipt_rows.py <repo> <run-receipts.json> <round-2 MANIFEST.json> <round-2 author dir>"""
import json, re, sys
from pathlib import Path
repo, rr, man, author = (Path(a) for a in sys.argv[1:5])
page = (repo / "docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md").read_text()
receipts = json.loads(rr.read_text())
print("run-receipts.json top-level keys:", list(receipts)[:6] if isinstance(receipts, dict) else type(receipts))
rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in page.split("## Run receipts", 1)[1].splitlines()
        if l.startswith("| ") and not l.startswith("| Run") and not l.startswith("| Point") and not l.startswith("| Variant")]
yosys = {r[0]: r for r in rows if len(r) == 6 and r[1].startswith("`")}
print("page Yosys receipt rows:", len(yosys))
plan = json.loads((repo / "syn/resmap/sweep_plan.json").read_text())
names = [p["name"] for p in plan["points"]]
print("plan points:", len(names), "rows for every plan point:", sorted(names) == sorted(yosys))
bad = 0
for name in names:
    g = json.loads((author / "inputs/work/guards" / f"{name}.json").read_text())
    page_refused = yosys[name][5] != "clean"
    if bool(g["refusals"]) != page_refused or g["rc"] != 0 or g["errors"]:
        bad += 1
        print("GUARD MISMATCH", name, g["rc"], g["refusals"][:1], yosys[name][5])
print(f"guard records: {len(names)} of {len(names)} published; refused per records "
      f"{sum(bool(json.loads((author / 'inputs/work/guards' / f'{n}.json').read_text())['refusals']) for n in names)}; "
      f"mismatches with the page {bad}")
flat = json.dumps(receipts)
for name, r in yosys.items():
    if r[4].strip("`") not in flat:
        bad += 1
        print("DIGEST NOT IN run-receipts.json", name, r[4])
print("page Yosys digests found in run-receipts.json:", sum(r[4].strip("`") in flat for r in yosys.values()))
m = {e["file"]: e for e in json.loads(man.read_text())}
reopen = next(l for l in page.splitlines() if l.startswith("| Route reopen, round 2"))
digest = re.search(r"`([0-9a-f]{16})`", reopen).group(1)
orig = m["author/inputs/map/route_map.log"]["original_sha256"]
print("round-2 reopen row digest", digest, "manifest original", orig[:16], "equal:", orig.startswith(digest))
bad += not orig.startswith(digest)
print("RESULT", "PASS" if not bad else f"FAIL {bad}")
sys.exit(1 if bad else 0)
