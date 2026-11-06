#!/usr/bin/env python3
"""Check that every Findings row of the committed page is traceable through --findings-dir.

Usage: findings_trace.py CLONE OUTDIR. Parses page rows and lane files, proves a one-to-one
match on (id, page), and proves each named line really carries the statement.
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

clone, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
done = subprocess.run(["python3", "-I", "scripts/docs_inventory.py", "--findings-dir", str(out)], cwd=clone,
                      capture_output=True, text=True, check=False)
print("findings-dir rc", done.returncode)
print(done.stdout.strip())
spec = importlib.util.spec_from_file_location("inv", clone / "scripts/docs_inventory.py")
inv = importlib.util.module_from_spec(spec)
sys.modules["inv"] = inv
spec.loader.exec_module(inv)
page = (clone / inv.OUTPUT).read_text(encoding="utf-8")
section, rows = "", []
for row in page.split("\n"):
    if row.startswith("## "):
        section = row[3:].strip()
    elif section == "Findings" and row.startswith("| D0-"):
        parts = inv.cells(row)
        rows.append((parts[0], inv.ROW_LINK_RE.match(parts[1]).group(1), parts[2], parts[3]))
lanes = []
for lane in sorted(out.glob("*.md")):
    text = lane.read_text(encoding="utf-8")
    for match in re.finditer(r"^## (D0-\d+): (.+):(\d+|\?)\n\n- Statement: (.*)\n- Contradicted by: (.*)\n- Correction: (.*)\n",
                             text, re.MULTILINE):
        lanes.append(match.groups())
print("page rows", len(rows), "lane entries", len(lanes))
print("Located values", sorted({r[2] for r in rows}))
print("rows missing from lanes", sorted({(r[0], r[1]) for r in rows} - {(e[0], e[1]) for e in lanes}))
print("lane entries missing from page", sorted({(e[0], e[1]) for e in lanes} - {(r[0], r[1]) for r in rows}))
print("duplicate (id, page) keys on the page", len(rows) - len({(r[0], r[1]) for r in rows}))
bad = []
for ident, path, number, statement, _, _ in lanes:
    if number == "?":
        bad.append((ident, path, "no line"))
        continue
    lines = (clone / path).read_text(encoding="utf-8", errors="replace").split("\n")
    window = " ".join(lines[int(number) - 1:int(number) + 5])
    if inv.needle_of(statement) not in inv.normal_form(window) and statement not in lines[int(number) - 1]:
        bad.append((ident, path, number))
print("named lines not carrying their statement", len(bad), bad[:10])
