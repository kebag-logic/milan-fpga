#!/usr/bin/env python3
"""Check that the gate's status-rule parser reads every Inventory and Findings row of the committed page.

Usage: python3 -I parse_coverage.py CLONE
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
import docs_inventory as d  # noqa: E402

page = (root / d.OUTPUT).read_text(encoding="utf-8")
data = json.loads((root / d.DATA).read_text(encoding="utf-8"))
section, inv, fnd, inv_skipped, fnd_skipped, esc = "", {}, {}, [], [], 0
for row in page.split("\n"):
    if row.startswith("## "):
        section = row[3:].strip()
        continue
    if not row.startswith("| ") or set(row) <= set("|- "):
        continue
    parts = d.cells(row)
    if "\\|" in row:
        esc += 1
    if section == "Inventory":
        m = d.ROW_LINK_RE.match(parts[0]) if len(parts) == 9 else None
        if m:
            inv[m.group(1)] = parts[5]
        elif parts and parts[0] != "Document":
            inv_skipped.append(row[:120])
    elif section == "Findings":
        m = d.ROW_LINK_RE.match(parts[1]) if len(parts) == 6 else None
        if m:
            fnd.setdefault(m.group(1), []).append(parts[0])
        elif parts and parts[0] not in ("ID",):
            fnd_skipped.append(row[:120])
pages_with = {f["page"] for f in data["findings"]}
print("sections:", [l[3:] for l in page.split("\n") if l.startswith("## ")])
print("inventory rows parsed:", len(inv), "skipped:", len(inv_skipped), inv_skipped[:3])
print("findings rows parsed:", sum(map(len, fnd.values())), "pages:", len(fnd), "skipped:", len(fnd_skipped), fnd_skipped[:3])
print("data findings:", len(data["findings"]), "data pages:", len(pages_with))
print("rows with escaped pipes:", esc)
print("data pages == listed pages:", pages_with == set(fnd))
print("status of pages with findings:", sorted({(p, inv.get(p)) for p in pages_with}))
print("current_with_findings(committed):", d.current_with_findings(page))
counts = {}
for v in inv.values():
    counts[v] = counts.get(v, 0) + 1
print("status counts:", counts)
