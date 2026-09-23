#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""R228-4: aggregate the per-mutant JSON receipts into one summary.

Usage: r228_4_summary.py <packet-dir>  (writes receipts/mutation-summary.json)
"""

import json
import sys
from pathlib import Path

packet = Path(sys.argv[1])
rows = []
for group in ("mutations-head", "mutations-prev", "gate1b", "prior-mutants-head"):
    for path in sorted((packet / "receipts" / group).glob("*.json")):
        d = json.loads(path.read_text())
        rows.append({"group": group, "id": d["id"], "kind": d["kind"],
                     "tree_head": d.get("tree_head"),
                     "models": d.get("models", d.get("reverts")),
                     "verdict": d["verdict"], "returncode": d["returncode"],
                     "killing_probe": d.get("killing_probe"),
                     "first_failure": (d.get("first_failure") or [""])[0][:240],
                     "gate_summary": d.get("gate_summary")})
(packet / "receipts" / "mutation-summary.json").write_text(json.dumps(rows, indent=1) + "\n")
for group in ("mutations-head", "mutations-prev", "gate1b", "prior-mutants-head"):
    sel = [r for r in rows if r["group"] == group]
    k = sum(r["verdict"] == "KILLED" for r in sel)
    s = sum(r["verdict"] == "SURVIVED" for r in sel)
    e = sum(r["verdict"] not in ("KILLED", "SURVIVED") for r in sel)
    print(f"{group}: {len(sel)} runs, {k} KILLED, {s} SURVIVED, {e} other")
    for r in sel:
        print(f"  {r['id']:42s} {r['verdict']:8s} {', '.join(r['killing_probe'] or []) or (r['first_failure'][:80] if r['verdict']=='KILLED' else '')}")
