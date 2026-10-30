#!/usr/bin/env python3
"""Print one page's numeric or normative statements with their mechanical results, compactly.

Usage: python3 -I show.py <ledger dir> <page> [width] [first-line] [last-line]
"""
import json
import sys
from pathlib import Path

d, page = Path(sys.argv[1]), sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 400
lo = int(sys.argv[4]) if len(sys.argv) > 4 else 0
hi = int(sys.argv[5]) if len(sys.argv) > 5 else 10 ** 9
auto = {(r["page"], r["line"]): r for r in map(json.loads, (d / "auto.jsonl").read_text().splitlines())}
for rec in map(json.loads, (d / "statements.jsonl").read_text().splitlines()):
    if rec["page"] != page or not (rec["numeric"] or rec["normative"]) or not lo <= rec["line"] <= hi:
        continue
    a = auto.get((page, rec["line"]), {}).get("auto", {})
    tags = ",".join(f"{k}{v.get('n', '')}" for k, v in a.items())
    text = rec["text"].replace("\n", " / ")
    print(f"{rec['line']}[{rec['kind'][0]}{'|' + tags if tags else ''}] {text[:width]}")
