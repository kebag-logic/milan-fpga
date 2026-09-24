#!/usr/bin/env python3
"""Compare this round's probe receipts with the previous round's, per case.
usage: compare_rounds.py <prev-receipts-dir> <this-receipts-dir> <stem>... """
import json, sys
from pathlib import Path
prev, cur = Path(sys.argv[1]), Path(sys.argv[2])
for stem in sys.argv[3:]:
    for mode in ("sdk", "absent"):
        a = cur / f"{stem}-head-{mode}.json"
        b = prev / f"{stem}-head-{mode}.json"
        now = {r["label"]: r for r in json.loads(a.read_text())["results"]}
        was = {r["label"]: r for r in json.loads(b.read_text())["results"]} if b.exists() else {}
        print(f"## {stem} {mode}: {len(now)} cases")
        for label, r in now.items():
            p = was.get(label)
            pv = p["verdict"] if p else "-"
            reason = r.get("reason", "")[:110].replace("\n", " ")
            flag = "" if pv == r["verdict"] else "  <-- CHANGED"
            print(f"  {pv:8} -> {r['verdict']:8} {label[:70]}{flag}")
            if r["verdict"] == "REFUSED":
                print(f"           {reason}")
