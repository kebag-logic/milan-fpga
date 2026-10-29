"""Re-point the line anchors of docs/SOURCE_EVIDENCE.md to the constructs
scripts/check_source_evidence.py expects. A construct that is not exactly
one stripped line of its file stops the script.

usage: repoint_anchors.py <repository root>
"""
import importlib.util
import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("cse", root / "scripts/check_source_evidence.py")
cse = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cse)
ledger_path = root / "docs/SOURCE_EVIDENCE.md"
rows = ledger_path.read_text().splitlines()
moved = 0
for i, row in enumerate(rows):
    if not row.startswith("|"):
        continue
    claim = row.split("|")[1].strip()
    targets = cse.EXPECTED.get(claim)
    if not targets:
        continue
    links = list(cse.ANCHOR.finditer(row))
    assert len(links) == len(targets), claim
    new = row
    for m, (source, construct) in reversed(list(zip(links, targets))):
        lines = (root / source).read_text().splitlines()
        hits = [n + 1 for n, l in enumerate(lines) if l.strip() == construct]
        assert len(hits) == 1, (claim, construct, hits)
        start, end = m.span(2)
        if new[start:end] != str(hits[0]):
            moved += 1
        new = new[:start] + str(hits[0]) + new[end:]
    rows[i] = new
ledger_path.write_text("\n".join(rows) + "\n")
print(moved, "anchors moved")
