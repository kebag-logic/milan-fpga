#!/usr/bin/env python3
"""Lane entries against the page's Findings rows, and each named line against its statement.

usage: line_truth848d.py <disposable clone> <scratch dir>
"""
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

root, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "scripts"))
sys.dont_write_bytecode = True
import docs_inventory as inv  # noqa: E402

subprocess.run(["python3", "-B", "scripts/docs_inventory.py", "--findings-dir", str(scratch)], cwd=root, check=True,
               capture_output=True)
entries = []
for lane in sorted(scratch.glob("*.md")):
    text = lane.read_text(encoding="utf-8")
    entries += re.findall(r"^## (D0-\d+): (.+):(\d+|\?)\n\n- Statement: (.*)$", text, re.M)
page = (root / inv.OUTPUT).read_text(encoding="utf-8").split("## Findings", 1)[1]
rows = []
for row in page.split("\n"):
    parts = inv.cells(row) if row.startswith("| D0-") else []
    if parts:
        link = inv.ROW_LINK_RE.match(parts[1])
        rows.append((parts[0], link.group(1), parts[2]))
print("entries", len(entries), "page rows", len(rows))
print("same (id, page) multiset:", Counter(e[:2] for e in entries) == Counter(r[:2] for r in rows))
flagged = sorted(r[:2] for r in rows if r[2] != "on page")
unlocated = sorted(e[:2] for e in entries if e[2] == "?")
print("unlocated", len(unlocated), "equal to the rows the page flags:", unlocated == flagged)
literal = normalised = wrong = 0
for ident, name, line, quote in entries:
    if line == "?":
        continue
    lines = (root / name).read_text(encoding="utf-8", errors="replace").split("\n")
    n = int(line) - 1
    if quote.replace("\\|", "|") in lines[n]:
        literal += 1
    elif inv.normal_form(quote).rstrip(".,;:") in inv.normal_form(" ".join(lines[n:n + 6])):
        normalised += 1
    else:
        wrong += 1
        print("WRONG", ident, name, line)
print(f"literal on the named line {literal}, normalised {normalised}, wrong {wrong}")
